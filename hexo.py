import subprocess

def execute_hexo_commands():
    # 进入特定的目录
    directory = r'D:\博客\hexo-blog'
    cmd = f'cd /d {directory} && echo hexo clean && hexo clean && echo hexo g && hexo g && echo hexo d && hexo d  && exit'

    # 打开cmd并执行命令
    subprocess.call(['start', 'cmd', '/k', cmd], shell=True)

execute_hexo_commands()