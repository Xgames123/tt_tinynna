export INSTALL_DIR := "~/ttsetup"

export PDK := "sky130A"
export LIBRELANE_TAG := "3.0.0rc1"
export PDK_ROOT := INSTALL_DIR + "/pdk"

export VENV_ACTIVATE := "source "+ INSTALL_DIR + "/venv/bin/activate"

run:
  #!/bin/bash
  $VENV_ACTIVATE
  ./tt/tt_tool.py --create-user-config
  ./tt/tt_tool.py --harden
  ./tt/tt_tool.py --print-warnings

[working-directory("test")]
test: test-setup
  #!/bin/bash
  $VENV_ACTIVATE
  make -B

[working-directory("test")]
test-gates: gate-test-setup
  #!/bin/bash
  $VENV_ACTIVATE
  make -B GATES=yes


setup:
  #!/bin/bash
  mkdir -p $INSTALL_DIR
  python3 -m venv $INSTALL_DIR/venv

  pip install librelane==$LIBRELANE_TAG
  pip install -r tt/requirements.txt


[working-directory("test")]
test-setup:
  #!/bin/bash
  $VENV_ACTIVATE
  export COCOTB_IGNORE_PYTHON_REQUIRES=1
  pip install -r requirements.txt

[working-directory("test")]
gate-test-setup: test-setup
  cp ../runs/wokwi/final/nl/*.nl.v gate_level_netlist.v

