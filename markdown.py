import os
import shutil
import sys
import io
import random

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def move_images(source_folder, target_folder):
    print(f"开始处理图片文件夹：{source_folder}")
    print()
    images = os.listdir(source_folder)
    if len(images) == 0:
        print(f"图片文件夹 {source_folder} 中没有图片文件。")
        print()
        return

    for image_name in images:
        image_path = os.path.join(source_folder, image_name)
        if os.path.isfile(image_path):
            print(f"正在处理图片：\033[31m{image_name}\033[0m")
            target_path = os.path.join(target_folder, image_name)

            if os.path.exists(target_path):
                print(f"目标文件夹中已存在同名图片文件：{target_path}")
                print("跳过当前图片。")
                print()
                continue

            shutil.move(image_path, target_path)
            print(f"已处理并移动图片：{target_path}")
            print()

            update_index_file(target_folder, image_name)

    print(f"图片文件夹 {source_folder} 处理完成。")
    print()


def update_index_file(folder, image_name):
    index_file_path = os.path.join(folder, "index.md")
    if not os.path.exists(index_file_path):
        print(f"未找到 {index_file_path} 文件。")
        return

    with open(index_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line number containing {% gallery %}
    gallery_line_index = -1
    for i, line in enumerate(lines):
        if '{% gallery %}' in line:
            gallery_line_index = i
            break

    if gallery_line_index == -1:
        print("未找到 {% gallery %} 行，请确保在 index.md 中存在该行。")
        return

    # Insert the new content after {% gallery %}, ensuring a newline
    new_content = f"![]({image_name})\n"
    lines.insert(gallery_line_index + 1, new_content)

    with open(index_file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    print(f"已更新 {index_file_path}")
    print()



def process_markdown_file(file_path, wakawaka_images_folder):
    file_name = os.path.basename(file_path)
    title = os.path.splitext(file_name)[0]
    print(f"正在处理Markdown文档：\033[31m{file_name}\033[0m")
    print("当前文章的categories是？")
    categories = input().encode(sys.stdin.encoding).decode(sys.stdin.encoding).replace("，", ",").split(",")
    categories = [category.strip() for category in categories]

    print("当前文章的tags是？")
    tags = input().encode(sys.stdin.encoding).decode(sys.stdin.encoding).replace("，", ",").split(",")
    tags = [tag.strip() for tag in tags]

    cover_image = get_random_image(wakawaka_images_folder)
    info = f"---\n"
    info += f"title: [{title}]\n"
    info += f"categories: {categories}\n"
    info += f"tags: {tags}\n"
    info += f"background: url(/img/wakawaka/{cover_image})\n"
    info += f"cover: {{ {cover_image} }}\n"
    info += f"---\n"

    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        file.seek(0, 0)
        file.write(info + "\n" + content)

    html_code = '<meta name="referrer" content="no-referrer">\n'

    with open(file_path, 'a', encoding='utf-8') as file:
        file.write("\n" + html_code)

    new_file_path = os.path.join(r"D:\博客\hexo-blog\source\_posts", file_name)

    if os.path.exists(new_file_path):
        print(f"目标文件夹中已存在同名文档：{new_file_path}")
        print("是否覆盖原始文档？(Y/N)")
        choice = input().strip().lower()
        if choice != "y":
            print("跳过当前文档。")
            return

    shutil.move(file_path, new_file_path)
    print(f"已处理并移动文件：{new_file_path}")
    print()


def get_random_image(folder):
    images = os.listdir(folder)
    if len(images) == 0:
        return ""
    return random.choice(images)


def main():
    drafts_folder = r"D:\博客\hexo-blog\source\_drafts"
    posts_folder = r"D:\博客\hexo-blog\source\_posts"
    wakawaka_images_folder = r"D:\博客\img\wakawaka"
    nsfw_images_folder = r"D:\博客\img\NSFW"
    wakawaka_target_folder = r"D:\博客\hexo-blog\source\img\wakawaka"
    nsfw_target_folder = r"D:\博客\hexo-blog\source\img\NSFW"

    move_images(wakawaka_images_folder, wakawaka_target_folder)
    move_images(nsfw_images_folder, nsfw_target_folder)

    while True:
        files = os.listdir(drafts_folder)
        if len(files) == 0:
            print("已处理完所有markdown文档。")
            break

        for file_name in files:
            file_path = os.path.join(drafts_folder, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith(".md"):
                process_markdown_file(file_path, wakawaka_target_folder)

        if len(os.listdir(posts_folder)) == 0:
            print("已处理完所有markdown文档。")
            break

        print("请切换到命令行窗口以继续处理剩余的markdown文档。")
        input("按回车键继续...")
        print()


if __name__ == "__main__":
    main()