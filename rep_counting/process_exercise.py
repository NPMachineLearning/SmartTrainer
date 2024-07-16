import argparse
from pathlib import Path
import process
from process import DEFAULT_OUTPUT_DIR

def main(root_path, file_ext, output_dir):
    root_dir = Path(root_path)
    if not root_dir.exists():
        raise Exception(f"{root_path} directory doesn't exists")
    for sub_dir in root_dir.iterdir():
        path = root_dir / sub_dir.name
        exercise_name = sub_dir.name
        examples = list(path.glob(f"*.{file_ext}"))
        if len(examples) == 0:
            raise Exception(f"{path} is empty, there must have 1 example")
        example_path = examples[0]
        process.main(example_path, exercise_name, output_dir)

if __name__ == "__main__":
    desc = """
    This program process all exercises in directory. Root directory contain
    one or more subdirectories where each subdirectories' name is exercise name.
    Each subdirectories must have 1 exercise example in video type such as mp4 or
    gif. Video file that is readable for OpenCv.
    """
    parser = argparse.ArgumentParser(prog="Processing exercise examples in directory",
                                     description=desc)
    parser.add_argument("--dir", help="Path to root directory where it contain exercise examples", required=True)
    parser.add_argument("--file_ext", help="Extension of file to look for e.g mp4, gif", required=True)
    parser.add_argument("--out", help="Output json config file directory", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    main(args.dir, args.file_ext, args.out)