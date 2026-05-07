#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

PYTHON_DIR="$SCRIPT_DIR/python"
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PY="$VENV_DIR/bin/python"
UV_DIR="$SCRIPT_DIR/.tools/uv/bin"
UV_BIN="$UV_DIR/uv"

ensure_uv() {
  if [ -x "$UV_BIN" ]; then
    return 0
  fi

  mkdir -p "$UV_DIR"

  if command -v curl >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="$UV_DIR" UV_NO_MODIFY_PATH=1 sh
  elif command -v wget >/dev/null 2>&1; then
    wget -qO- https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="$UV_DIR" UV_NO_MODIFY_PATH=1 sh
  else
    echo "Neither curl nor wget was found. Unable to download the bundled runtime."
    return 1
  fi

  [ -x "$UV_BIN" ]
}

ensure_runtime() {
  if [ -x "$VENV_PY" ]; then
    return 0
  fi

  if command -v python3 >/dev/null 2>&1; then
    echo "Creating runtime with local Python..."
    python3 -m venv "$VENV_DIR" && return 0
  elif command -v python >/dev/null 2>&1; then
    echo "Creating runtime with local Python..."
    python -m venv "$VENV_DIR" && return 0
  fi

  echo "Python was not found. Creating a self-contained runtime..."
  ensure_uv || return 1
  "$UV_BIN" venv "$VENV_DIR" --python 3.12
}

ensure_requirements() {
  "$VENV_PY" -c "import ccl_chromium_reader" >/dev/null 2>&1 && return 0
  echo "Installing dependencies..."
  "$VENV_PY" "$PYTHON_DIR/bootstrap_dependencies.py"
}

ensure_runtime || {
  echo
  echo "Runtime creation failed."
  echo
  exit 1
}

ensure_requirements || {
  echo
  echo "Dependency installation failed."
  echo "This launcher installs ccl_chromium_reader from GitHub source archives."
  echo "Network access to github.com and codeload.github.com is required."
  echo
  exit 1
}

"$VENV_PY" "$PYTHON_DIR/run_teams_pipeline.py" --open-browser "$@"
STATUS=$?
echo
exit $STATUS
