import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        if filename.startswith('.'):
            continue
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            if not filename.lower().endswith('.md'):
                continue
            dest_path = Path(dest_path).with_suffix('.html')
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
