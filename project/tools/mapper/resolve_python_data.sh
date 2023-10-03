# Copyright (c) 2021 Horizon Robotics.All Rights Reserved.
#
# The material in this file is confidential and contains trade secrets
# of Horizon Robotics Inc. This is proprietary information owned by
# Horizon Robotics Inc. No part of this work may be disclosed,
# reproduced, copied, transmitted, or used in any way for any purpose,
# without the express written permission of Horizon Robotics Inc.

basepath=$(
  cd $(dirname $0)
  pwd
)

cp "${basepath}"/../../../../../horizon_tc_ui/data/dataset.py "${basepath}"
cp "${basepath}"/../../../../../horizon_tc_ui/data/dataloader.py "${basepath}"
cp "${basepath}"/../../../../../horizon_tc_ui/data/transformer.py "${basepath}"
cp "${basepath}"/../../../../../horizon_tc_ui/data/dataset_consts.py "${basepath}"
