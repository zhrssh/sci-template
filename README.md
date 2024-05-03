# Sci-template

This template made by **Zherish Galvin Mayordo** is tailored for data enthusiasts. The modules for this template were originally used for a specific deep learning study that were redesigned to be flexible and modular.

## How to use this template

1. Make sure to install Anaconda or Miniconda before using this template. You can install either of them at [this link](https://www.anaconda.com/).
2. Create a new environment for this template using the command `conda env create -f environment.yml -n [ENVIRONMENT_NAME]`, for CUDA-enabled systems, OR `conda env create -f environment-noncuda.yml -n [ENVIRONMENT_NAME]`, for non-CUDA-enabled systems.
3. Activate the new environment: `conda activate [ENVIRONMENT_NAME]`.
4. Verify that the new environment was installed correctly: `conda list`
5. Once verified, run `setup.cfg` using `pip install`

_Note: This package already includes tensorflow and scikit-learn._ <br>
_Note: This package is created using Windows 10 operating system._ <br>
_Note: You can also verify if tensorflow is installed properly using the command: `python -c "import tensorflow as tf; print(tf.config.list_physical_devices())"`_

## Author details

If you want to reach out to me, here's my contact details:

**Name**: Zherish Galvin Mayordo <br>
**Email**: zherishatbusiness@gmail.com <br>
**LinkedIn**: https://www.linkedin.com/in/zgmayordo <br>

#### If you want to contribute, here are the committing guidelines:

1. **[fix]**: For bug fixes.
2. **[update]**: For updating code's functionality.
3. **[feat]**: For adding new feature/s.
4. **[style]**: For changes that do not affect the code's functionality (e.g., formatting, spacing).
5. **[docs]**: For documentation changes.
6. **[refactor]**: For code refactoring without changing its external behavior.
7. **[perf]**: For performance improvements.
8. **[chore]**: For maintenance tasks, tooling changes, or other non-code changes.
9. **[dependency]**: For updates or changes related to dependencies.
10. **[security]**: For security-related changes.
11. **[cleanup]**: For removing redundant code or files.
12. **[merge]**: For merge commits.
