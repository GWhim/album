#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from urllib.parse import quote

EXCLUDE_DIRS = ['.git', 'docs', '.vscode', 'overrides', '.github', 'script']
README_MD = ['README.md', 'readme.md', 'index.md']
INDEX_FILE = 'index.md'

IMAGE_EXTS = ['jpg', 'png', 'svg', 'jpeg', 'gif', 'webp']


def list_image(course: str):
    imagelist_text = f'# {os.path.basename(course)}\n'

    for root, dirs, files in os.walk(course):
        files.sort()
        readme_path = '{}/{}'.format(root, INDEX_FILE)
        level = root.replace(course, '').count(os.sep)
        for f in files:
            if f.split('.')[-1].lower() in IMAGE_EXTS:
                imagelist_text += '![]({}){{ width="200" }}\n'.format(
                    os.path.join(os.path.basename(root), f))
    return imagelist_text, readme_path


def generate_md(course: str, filelist_texts: str, readme_path: str, topic: str):
    final_texts = ['\n\n'.encode(), filelist_texts.encode()]
    topic_path = os.path.join('docs', topic)
    if not os.path.isdir(topic_path):
        os.mkdir(topic_path)
    with open(os.path.join(topic_path, '{}.md'.format(course)), 'wb') as file:
        file.writelines(final_texts)


if __name__ == '__main__':
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    if not os.path.isdir('docs'):
        os.mkdir('docs')
    if os.path.exists('CNAME'):
        shutil.copy('CNAME', 'docs/CNAME')
    topics = list(
        filter(lambda x: os.path.isdir(x) and (x not in EXCLUDE_DIRS),
               os.listdir('.')))  # list topics
    if os.path.exists('CNAME'):
        shutil.copy('CNAME', 'docs/CNAME')
    for topic in topics:
       
        topic_path = os.path.join('.', topic)
        target_path = os.path.join('docs', topic)
        
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        shutil.copytree(topic_path, target_path)

        topic_item = list(
            filter(
                lambda x: os.path.isdir(os.path.join(topic_path, x)) and
                (x not in EXCLUDE_DIRS), os.listdir(topic_path)))

        for item in topic_item:
            item_path = os.path.join(".", topic, item)
            imagelist_text, readme_path = list_image(item_path)
            generate_md(item, imagelist_text, readme_path, topic)

    with open('README.md', 'rb') as file:
        mainreadme_lines = file.readlines()

    with open('docs/index.md', 'wb') as file:
        file.writelines(mainreadme_lines)
