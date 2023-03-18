var Config = {
  handSkeletonKey: [
    'moonBone',

    'thumbsMetacarpal',
    'thumbsProximalPhalanx',
    'thumbsMiddlePhalanx',
    'thumbsDistalPhalanx',

    'indexMetacarpal',
    'indexProximalPhalanx',
    'indexMiddlePhalanx',
    'indexDistalPhalanx',

    'middleMetacarpal',
    'middleProximalPhalanx',
    'middleMiddlePhalanx',
    'middleDistalPhalanx',

    'ringMetacarpal',
    'ringProximalPhalanx',
    'ringMiddlePhalanx',
    'ringDistalPhalanx',

    'littleMetacarpal',
    'littleProximalPhalanx',
    'littleMiddlePhalanx',
    'littleDistalPhalanx',
  ],
  skeletonKey: [
    'nose',
    'leftEye',
    'rightEye',

    'leftEar',
    'rightEar',

    'leftShoulder',
    'rightShoulder',

    'leftElbow',
    'rightElbow',

    'leftWrist',
    'rightWrist',

    'leftHip',
    'rightHip',

    'leftKnee',
    'rightKnee',

    'leftAnkle',
    'rightAnkle'
  ],
  glasses: {
    undefined: false,
    1: 'Glasses',
    2: 'SunGlssses',
  },
  breathingMask: {
    undefined: false,
    1: 'Mask'
  },
  gender: {
    undefined: '女性',
    1: '男性'
  },
  age: {
    undefined: '年龄: 0-6',
    1: '年龄: 6-12',
    2: '年龄: 12-18',
    3: '年龄: 18-28',
    4: '年龄: 28-35',
    5: '年龄: 35-45',
    6: '年龄: 45-55',
    7: '年龄: 55-100'
  }
};


var _config = {
  attr_tag_num: 13,
  tags: {
    '0': {
      name: 'upper',
      labels: [
        'long_sleeve',
        'short_sleeve',
        'dress',
        'overcoat',
        'short_downjacket',
        'other'
      ]
    },
    '1': {
      name: 'lower',
      labels: ['trousers', 'short_pants', 'dress', 'overcoat', 'other']
    },
    '2': {
      name: 'gender',
      labels: ['male', 'female', 'unknown']
    },
    '3': {
      name: 'hair',
      labels: ['no', 'yes', 'unknown']
    },
    '4': {
      name: 'hat',
      labels: ['no', 'yes', 'unknown']
    },
    '5': {
      name: 'glasses',
      labels: ['no', 'yes', 'unknown']
    },
    '6': {
      name: 'mask',
      labels: ['no', 'yes', 'unknown']
    },
    '7': {
      name: 'bag',
      labels: ['no', 'Backpack', 'Single_Shoulder_Bag', 'unknown']
    },
    '8': {
      name: 'hand_carry_things',
      labels: ['no', 'yes', 'unknown']
    },
    '9': {
      name: 'phone',
      labels: ['no', 'yes', 'unknown']
    },
    '10': {
      name: 'umbrella',
      labels: ['no', 'yes', 'unknown']
    },
    '11': {
      name: 'upper_part_color',
      labels: [
        'Black',
        'White',
        'Gray',
        'Red',
        'Pink',
        'Yellow ',
        'Orange',
        'Brown',
        'Blue',
        'Green',
        'Purple',
        'Colorful',
        'other'
      ]
    },
    '12': {
      name: 'lower_part_color',
      labels: [
        'Black',
        'White',
        'Gray',
        'Red',
        'Pink',
        'Yellow ',
        'Orange',
        'Brown',
        'Blue',
        'Green',
        'Purple',
        'Colorful',
        'other'
      ]
    }
  }
};
