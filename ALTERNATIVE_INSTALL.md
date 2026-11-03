# Isolated Windows package test

This documents an independently installed package environment on one RTX 5070 Ti 16 GB / approximately 64 GB RAM machine. It is not a universal installer or a guarantee for other operating systems, drivers or model conversions. Read README.md for the current inference-test result.

The historical `2.14.0.dev20260705+cu130` Torch wheel was not found in the checked official nightly index. The alternative uses Python 3.13.12, Torch 2.13.0+cu130, torchvision 0.28.0+cu130 and torchaudio 2.11.0+cu130. CUDA matrix multiplication, audio resampling and package dependency checks passed. ComfyUI source was a clean tracked snapshot at `87465b8f1f64a27a46f16f22b13b410494dca66d` (0.34.3), taken from the existing checkout; downloading that source again was not part of this test.

## Package selection

Use a **new, separate Python 3.13 environment**. The test extracted CPython 3.13.12 from its [official NuGet package](https://www.nuget.org/packages/python/3.13.12), without changing registry, system PATH or the production environment. Python [documents this distribution](https://docs.python.org/3.13/using/windows.html#the-nuget-org-packages).

Commands below use `python` to mean that new environment's interpreter. Use its full path; do not run them against an existing production installation. `COMFY_SOURCE` means the separate source snapshot above, and `KIT` means this repository.

```text
python -m pip install --index-url https://pypi.org/simple --only-binary=:all: numpy==2.4.6 opencv-python==5.0.0.93
python -m pip install --index-url https://download.pytorch.org/whl/cu130 --only-binary=:all: torch==2.13.0 torchvision==0.28.0
python -m pip install --index-url https://pypi.org/simple --only-binary=:all: -c KIT/isolated-constraints.txt -r COMFY_SOURCE/requirements.txt https://download-r2.pytorch.org/whl/cu130/torchaudio-2.11.0%2Bcu130-cp313-cp313-win_amd64.whl
python -m pip check
```

These are the package arguments used in the test. Additional local logging/report flags and a preservation wrapper retained installer temporary files. The first attempt's temporary-folder probe conflicted with that wrapper; specifying a new temporary directory explicitly resolved it. Normal pip may clean its own temporary files. No files were deleted in this trial. Full observed package versions are in ISOLATED_ENVIRONMENT_TEST.json; the constraints file fixes the core combination, not every transitive package.

## Separate server

Use new input, output, temporary, user/database and cache directories, a free local port, and an isolated model-search configuration referencing existing authorized weights. Do not copy production settings blindly or start competing GPU jobs. The test used `--use-pytorch-cross-attention`, `--cache-none`, `--reserve-vram 3`, `--vram-headroom 2`, `--disable-all-custom-nodes` and `--disable-api-nodes`. SageAttention and Triton were not installed. The H3 core graph does not need the optional camera custom node.

The test disabled ComfyUI's temporary cleanup in memory and added a deletion-blocking Python audit hook; source files were not patched. These preservation measures are additional test infrastructure, not an automatically installed feature of this kit.

Follow QUICKSTART with the new server URL and its actual input/output folders. Run doctor after the server says it is ready. One early doctor call failed with connection refused while the first startup was still importing dependencies; retrying after startup succeeded. Do not confuse a startup delay with a missing model or send duplicate inference jobs.

## Scope

Existing model files, NVIDIA driver 610.88 and FFmpeg/ffprobe 8.1.1 were reused. The test did not install a new driver, acquire weights afresh, automatically accept model terms, create the guide automatically or validate browser/canvas interaction. A successful render does not establish exact identity, acting, geometry or cross-machine reproducibility.
