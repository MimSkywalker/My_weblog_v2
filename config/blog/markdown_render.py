import re

import bleach
import markdown as md_lib
import yaml
from bs4 import BeautifulSoup
import copy

MARKDOWN_EXTENSIONS = [
    'extra', 'codehilite', 'toc', 'nl2br', 'sane_lists', 'admonition',
]
MARKDOWN_EXTENSION_CONFIGS = {
    'codehilite': {'css_class': 'codehilite', 'guess_lang': False},
    'toc': {'permalink': False},
}

ALLOWED_TAGS = [
    'p', 'br', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'em', 'b', 'i', 'u', 's', 'del', 'mark',
    'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'span', 'div',
    'a', 'img', 'figure', 'figcaption',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'sup', 'sub', 'dl', 'dt', 'dd', 'abbr',
    'details', 'summary',
]
ALLOWED_ATTRS = {
    '*': ['class', 'id', 'dir'],
    'a': ['href', 'title', 'rel', 'target'],
    'img': ['src', 'alt', 'title', 'loading', 'width', 'height'],
    'ol': ['start'],
    'td': ['align', 'colspan', 'rowspan', 'data-label'],
    'th': ['align', 'colspan', 'rowspan'],
    'abbr': ['title'],
}
FRONT_MATTER_RE = re.compile(r'^---\s*\n(.*?\n)?---\s*\n', re.DOTALL)

DEFAULT_SETTINGS = {
    'direction': 'rtl',
    'font_size': 'md',   # sm | md | lg
    'justify': False,
}

RTL_CHAR_RE = re.compile(
    r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
)
LTR_CHAR_RE = re.compile(r'[A-Za-z]')


def _extract_front_matter(raw_markdown):
    settings = DEFAULT_SETTINGS.copy()
    match = FRONT_MATTER_RE.match(raw_markdown or '')

    if not match:
        return settings, raw_markdown

    try:
        parsed = yaml.safe_load(match.group(1) or '') or {}
    except yaml.YAMLError:
        parsed = {}

    if isinstance(parsed, dict):
        if parsed.get('direction') in ('rtl', 'ltr'):
            settings['direction'] = parsed['direction']
        if parsed.get('font_size') in ('sm', 'md', 'lg'):
            settings['font_size'] = parsed['font_size']
        settings['justify'] = bool(parsed.get('justify', False))

    body = raw_markdown[match.end():]
    return settings, body


def _first_strong_direction(text):
    for ch in text:
        if RTL_CHAR_RE.match(ch):
            return 'rtl'
        if LTR_CHAR_RE.match(ch):
            return 'ltr'
    return None


def _process_html(html):
    """
    یه پاس روی HTML رندرشده:
    ۱) img:N رو به URL واقعی + (در صورت وجود کپشن) به figure/figcaption تبدیل می‌کنه
    ۲) روی li/p/td/th/blockquote/headingها بر اساس زبان خودشون dir واقعی ست می‌کنه
    """
    from .models import PostImage  # import محلی برای جلوگیری از circular import

    soup = BeautifulSoup(html, 'html.parser')

    for img in soup.find_all('img'):
        src = img.get('src', '')
        m = re.match(r'^img:(\d+)$', src)
        if not m:
            continue

        try:
            post_image = PostImage.objects.get(pk=m.group(1))
        except PostImage.DoesNotExist:
            img['src'] = ''
            continue

        img['src'] = post_image.image.url
        img['loading'] = 'lazy'
        if not img.get('alt'):
            img['alt'] = post_image.caption or ''

        if post_image.caption:
            figure = soup.new_tag('figure', **{'class': 'bd-md-figure'})
            img.wrap(figure)
            figcaption = soup.new_tag(
                'figcaption', **{'class': 'bd-md-caption'})
            figcaption.string = post_image.caption
            figure.append(figcaption)

            parent = figure.parent
            # اگه img تنها محتوای یه <p> بوده، پاراگراف رو باز می‌کنیم تا
            # <p><figure>...</figure></p> نامعتبر ساخته نشه
            if parent and parent.name == 'p' and parent.get_text(strip=True) == '':
                parent.unwrap()
    for table in soup.find_all('table'):
        header_cells = table.select(
            'thead th') or table.select('tr:first-child th')
        headers = [th.get_text(strip=True) for th in header_cells]

        body_rows = table.select('tbody tr') or table.find_all('tr')[1:]
        for row in body_rows:
            cells = row.find_all('td')
            for i, td in enumerate(cells):
                if i < len(headers) and headers[i]:
                    td['data-label'] = headers[i]

        cards = _build_table_card_accordion(soup, table)
        if cards is not None:
            table.insert_after(cards)

        scroll_wrapper = soup.new_tag('div', **{'class': 'bd-table-scroll'})
        table.wrap(scroll_wrapper)


        scroll_wrapper = soup.new_tag('div', **{'class': 'bd-table-scroll'})
        table.wrap(scroll_wrapper)
    for tag in soup.find_all(
        ['li', 'p', 'td', 'th', 'blockquote', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    ):
        direction = _first_strong_direction(tag.get_text(strip=True))
        if direction:
            tag['dir'] = direction

    return str(soup)


def render_post_content(raw_markdown):
    if not raw_markdown:
        return ''

    settings, body = _extract_front_matter(raw_markdown)

    html = md_lib.markdown(
        body,
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWN_EXTENSION_CONFIGS,
    )
    html = _process_html(html)

    wrapper_classes = f"bd-md bd-fs-{settings['font_size']}"
    if settings['justify']:
        wrapper_classes += ' bd-justify'

    wrapped = f'<div class="{wrapper_classes}" dir="{settings["direction"]}">{html}</div>'

    return bleach.clean(
        wrapped,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
    )


def _build_table_card_accordion(soup, table):
    """هر ردیف جدول رو به یه کارت آکاردئونی (details/summary) تبدیل می‌کنه.
    ستون اول → عنوان کارت (summary). بقیه‌ی ستون‌ها → لیست label/value."""
    header_cells = table.select(
        'thead th') or table.select('tr:first-child th')
    headers = [th.get_text(strip=True) for th in header_cells]
    if len(headers) < 2:
        return None

    body_rows = table.select('tbody tr') or table.find_all('tr')[1:]
    if not body_rows:
        return None

    container = soup.new_tag('div', **{'class': 'bd-table-cards'})

    for row in body_rows:
        cells = row.find_all('td')
        if not cells:
            continue

        details = soup.new_tag('details', **{'class': 'bd-tc-card'})

        summary = soup.new_tag('summary', **{'class': 'bd-tc-summary'})
        title_span = soup.new_tag('span', **{'class': 'bd-tc-summary-text'})
        first_dir = cells[0].get('dir')
        if first_dir:
            title_span['dir'] = first_dir
        for child in cells[0].contents:
            title_span.append(copy.deepcopy(child))
        if not title_span.get_text(strip=True):
            title_span.string = '—'
        summary.append(title_span)
        summary.append(soup.new_tag(
            'i', **{'class': 'fa-solid fa-chevron-down bd-tc-chevron'}))
        details.append(summary)

        body = soup.new_tag('div', **{'class': 'bd-tc-body'})
        for i, td in enumerate(cells[1:], start=1):
            if i >= len(headers):
                continue

            row_el = soup.new_tag('div', **{'class': 'bd-tc-row'})

            label_el = soup.new_tag('span', **{'class': 'bd-tc-label'})
            label_el.string = headers[i]
            row_el.append(label_el)

            value_el = soup.new_tag('span', **{'class': 'bd-tc-value'})
            value_dir = td.get('dir')
            if value_dir:
                value_el['dir'] = value_dir
            for child in td.contents:
                value_el.append(copy.deepcopy(child))
            if not value_el.get_text(strip=True):
                value_el.string = '—'
            row_el.append(value_el)

            body.append(row_el)

        details.append(body)
        container.append(details)

    return container
