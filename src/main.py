"""简单的 JMComic 示例 CLI

此脚本尽量不假设 jmcomic 的具体 API，而是提供两个简单命令：
  --version: 打印 jmcomic 包的版本（如果存在）或模块信息
  --list: 尝试调用常见的列出漫画接口（如果存在），否则列出模块属性供调试

打包时使用 PyInstaller 将此脚本打包为单文件可执行程序。
"""
import argparse
import sys


def probe_jmcomic():
    try:
        import jmcomic
    except Exception as e:
        return None, e
    return jmcomic, None


def main():
    parser = argparse.ArgumentParser(description="JMComic 简易客户端")
    parser.add_argument("--version", action="store_true", help="打印 jmcomic 包的版本或信息")
    parser.add_argument("--list", action="store_true", help="尝试列出可用漫画（如果 jmcomic 提供此功能）")
    args = parser.parse_args()

    jmcomic, err = probe_jmcomic()
    if jmcomic is None:
        print("未能导入 jmcomic：", err)
        print("请先运行：pip install -r requirements.txt")
        sys.exit(1)

    if args.version:
        ver = getattr(jmcomic, "__version__", None)
        if ver:
            print("jmcomic version:", ver)
        else:
            # 如果没有 __version__，展示模块路径和一些属性
            print("jmcomic module loaded from:", getattr(jmcomic, "__file__", "<built-in>"))
            print("模块属性示例：", ", ".join(sorted([a for a in dir(jmcomic) if not a.startswith("__")])[:20]))
        return

    if args.list:
        # 尝试常见接口名的几种尝试：list_comics, get_comics, search
        for name in ("list_comics", "get_comics", "search", "list"):
            fn = getattr(jmcomic, name, None)
            if callable(fn):
                try:
                    print(f"调用 {name}()，结果（截取）:")
                    result = fn()
                    # 保护性展示：如果是可迭代，展示前 10 项
                    if hasattr(result, "__iter__") and not isinstance(result, (str, bytes)):
                        out = []
                        for i, it in enumerate(result):
                            if i >= 10:
                                break
                            out.append(repr(it))
                        print("[", ", ".join(out), "]")
                    else:
                        print(repr(result))
                except TypeError:
                    print(f"函数 {name} 需要参数，跳过自动调用。可改造脚本以传参。")
                except Exception as e:
                    print(f"调用 {name}() 时出错：", e)
                return

        # 如果没有已知接口，打印模块可用属性帮助用户进行下一步
        print("未检测到常见的列举接口 (list_comics/get_comics/search)。jmcomic 模块的属性示例：")
        attrs = [a for a in dir(jmcomic) if not a.startswith("__")]
        print("\n".join(attrs[:200]))
        return

    # 如果没有参数，显示欢迎信息
    print("欢迎使用 JMComic 程序！")
    print("运行 --help 查看可用选项。如需打包成 .exe，请运行 build 脚本。")


if __name__ == "__main__":
    main()