def main():
    try:
        from utils.dependency import CheckDependencies
        from preprocess.preprocess import pre_process_full
    except ImportError as e:
        print(e)
        raise RuntimeError('please cd to src/ folder, then run \n`python -m tests.test_utils`')
    CheckDependencies()
    master_dir = './tests/data'
    root_dir = './tests/data/hierarchical_data'
    
    pre_process_full(root_dir,quiet=False)

    print('Success!')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Exception occurs while testing: {e}')