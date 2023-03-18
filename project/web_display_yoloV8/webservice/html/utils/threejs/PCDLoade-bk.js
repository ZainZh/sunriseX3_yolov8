/**
 * @author Filipe Caixeta / http://filipecaixeta.com.br
 * @author Mugen87 / https://github.com/Mugen87
 *
 * Description: A THREE loader for PCD ascii and binary files.
 *
 * Limitations: Compressed binary files are not supported.
 *
 */

THREE.PCDLoader = function (manager, callback, size = 1.0) {

  this.manager = (manager !== undefined) ? manager : THREE.DefaultLoadingManager;
  // console.log(manager, 'manager');
  this.littleEndian = true;
  this.callback = callback;
  this.size = size;

};


THREE.PCDLoader.prototype = {

  constructor: THREE.PCDLoader,

  load: function (url, onLoad, onProgress, onError) {

    var scope = this;

    var loader = new THREE.FileLoader(scope.manager);
    loader.setPath(scope.path);
    loader.setResponseType('arraybuffer');
    loader.load(url, function (data) {

      try {

        onLoad(scope.parse(data, url));

      } catch (e) {

        if (onError) {

          onError(e);

        } else {

          throw e;

        }

      }

    }, onProgress, onError);

  },

  setPath: function (value) {

    this.path = value;
    return this;

  },

  parse: function (data, url) {

    var scope = this;
    function parseHeader(data) {

      var PCDheader = {};
      var result1 = data.search(/[\r\n]DATA\s(\S*)\s/i);
      var result2 = /[\r\n]DATA\s(\S*)\s/i.exec(data.substr(result1 - 1));

      PCDheader.data = result2[1];
      PCDheader.headerLen = result2[0].length + result1;
      PCDheader.str = data.substr(0, PCDheader.headerLen);

      // remove comments

      PCDheader.str = PCDheader.str.replace(/\#.*/gi, '');

      // parse

      PCDheader.version = /VERSION (.*)/i.exec(PCDheader.str);
      PCDheader.fields = /FIELDS (.*)/i.exec(PCDheader.str);
      PCDheader.size = /SIZE (.*)/i.exec(PCDheader.str);
      PCDheader.type = /TYPE (.*)/i.exec(PCDheader.str);
      PCDheader.count = /COUNT (.*)/i.exec(PCDheader.str);
      PCDheader.width = /WIDTH (.*)/i.exec(PCDheader.str);
      PCDheader.height = /HEIGHT (.*)/i.exec(PCDheader.str);
      PCDheader.viewpoint = /VIEWPOINT (.*)/i.exec(PCDheader.str);
      PCDheader.points = /POINTS (.*)/i.exec(PCDheader.str);

      // evaluate

      if (PCDheader.version !== null)
        PCDheader.version = parseFloat(PCDheader.version[1]);

      if (PCDheader.fields !== null)
        PCDheader.fields = PCDheader.fields[1].split(' ');

      if (PCDheader.type !== null)
        PCDheader.type = PCDheader.type[1].split(' ');

      if (PCDheader.width !== null)
        PCDheader.width = parseInt(PCDheader.width[1]);

      if (PCDheader.height !== null)
        PCDheader.height = parseInt(PCDheader.height[1]);

      if (PCDheader.viewpoint !== null)
        PCDheader.viewpoint = PCDheader.viewpoint[1];

      if (PCDheader.points !== null)
        PCDheader.points = parseInt(PCDheader.points[1], 10);

      if (PCDheader.points === null)
        PCDheader.points = PCDheader.width * PCDheader.height;

      if (PCDheader.size !== null) {

        PCDheader.size = PCDheader.size[1].split(' ').map(function (x) {

          return parseInt(x, 10);

        });

      }

      if (PCDheader.count !== null) {

        PCDheader.count = PCDheader.count[1].split(' ').map(function (x) {

          return parseInt(x, 10);

        });

      } else {

        PCDheader.count = [];

        for (var i = 0, l = PCDheader.fields.length; i < l; i++) {

          PCDheader.count.push(1);

        }

      }

      PCDheader.offset = {};

      var sizeSum = 0;

      for (var i = 0, l = PCDheader.fields.length; i < l; i++) {

        if (PCDheader.data === 'ascii') {

          PCDheader.offset[PCDheader.fields[i]] = i;

        } else {

          PCDheader.offset[PCDheader.fields[i]] = sizeSum;
          sizeSum += PCDheader.size[i] * PCDheader.count[i];

        }

      }

      // for binary only

      PCDheader.rowSize = sizeSum;

      return PCDheader;

    }

    var textData = THREE.LoaderUtils.decodeText(data);

    // parse header (always ascii format)

    var PCDheader = parseHeader(textData);

    // parse data

    var position = [];
    var normal = [];
    var color = [];

    // ascii

    if (PCDheader.data === 'ascii') {

      var offset = PCDheader.offset;
      var pcdData = textData.substr(PCDheader.headerLen);
      var lines = pcdData.split('\n');

      for (var i = 0, l = lines.length; i < l; i++) {

        if (lines[i] === '') continue;

        var line = lines[i].split(' ');

        if (offset.x !== undefined) {

          position.push(parseFloat(line[offset.x]));
          position.push(parseFloat(line[offset.z]));
          position.push(-parseFloat(line[offset.y]));

        }

        // if ( offset.rgb !== undefined ) {

        // 	var rgb = parseFloat( line[ offset.rgb ] );
        // 	var r = ( rgb >> 16 ) & 0x0000ff;
        // 	var g = ( rgb >> 8 ) & 0x0000ff;
        // 	var b = ( rgb >> 0 ) & 0x0000ff;
        // 	color.push( r / 255, g / 255, b / 255 );

        // }

        if (offset.r !== undefined) {

          color.push(parseInt(line[offset.r], 10));
          color.push(parseInt(line[offset.g], 10));
          color.push(parseInt(line[offset.b], 10));

        }

        if (offset.rgb !== undefined) {

          var c = new Float32Array([parseFloat(line[offset.rgb])]);
          var dataview = new DataView(c.buffer, 0);
          color.push(dataview.getUint8(0) / 255.0);
          color.push(dataview.getUint8(1) / 255.0);
          color.push(dataview.getUint8(2) / 255.0);

        } else {
          color.push(1.0);
          color.push(1.0);
          color.push(1.0);
        }

        if (offset.normal_x !== undefined) {

          normal.push(parseFloat(line[offset.normal_x]));
          normal.push(parseFloat(line[offset.normal_y]));
          normal.push(parseFloat(line[offset.normal_z]));

        }

      }

    }

    // binary

    if (PCDheader.data === 'binary_compressed') {

      console.error('THREE.PCDLoader: binary_compressed files are not supported');
      return;

    }

    if (PCDheader.data === 'binary') {

      let dataview = new DataView(data, PCDheader.headerLen);
      let offset = PCDheader.offset;
      const downSampleRatio = 4;

      for (let i = 0, row = 0; i < PCDheader.points; i += downSampleRatio, row += (downSampleRatio * PCDheader.rowSize)) {

        if (offset.x !== undefined) {

          position.push(dataview.getFloat32(row + offset.x, this.littleEndian));
          position.push(dataview.getFloat32(row + offset.z, this.littleEndian));
          position.push(-dataview.getFloat32(row + offset.y, this.littleEndian));
        }

        if (offset.label !== undefined) {
          const label = dataview.getUint8(row + offset.label, this.littleEndian);
          const rgbarray = findPointCloudColorby16Label(label);
          color.push(rgbarray[0] / 255.0);
          color.push(rgbarray[1] / 255.0);
          color.push(rgbarray[2] / 255.0);
        } else {
          console.log('asasasa');
          color.push(1.0);
          color.push(1.0);
          color.push(1.0);
        }

        // if (offset.rgb !== undefined) {

        // 	color.push(dataview.getUint8(row + offset.rgb + 0) / 255.0);
        // 	color.push(dataview.getUint8(row + offset.rgb + 1) / 255.0);
        // 	color.push(dataview.getUint8(row + offset.rgb + 2) / 255.0);

        // } else if (offset.r !== undefined) {
        // 	color.push(dataview.getUint8(row + offset.r, this.littleEndian) / 255.0);
        // 	color.push(dataview.getUint8(row + offset.g, this.littleEndian) / 255.0);
        // 	color.push(dataview.getUint8(row + offset.b, this.littleEndian) / 255.0);
        // }

        if (offset.normal_x !== undefined) {

          normal.push(dataview.getFloat32(row + offset.normal_x, this.littleEndian));
          normal.push(dataview.getFloat32(row + offset.normal_y, this.littleEndian));
          normal.push(dataview.getFloat32(row + offset.normal_z, this.littleEndian));

        }

      }

    }

    // build geometry

    var geometry = new THREE.BufferGeometry();

    if (position.length > 0) geometry.addAttribute('position', new THREE.Float32BufferAttribute(position, 3));
    if (normal.length > 0) geometry.addAttribute('normal', new THREE.Float32BufferAttribute(normal, 3));
    if (color.length > 0) geometry.addAttribute('color', new THREE.Float32BufferAttribute(color, 3));

    geometry.computeBoundingSphere();

    // build material

    // console.log(scope.size, 'this.size');
    let material = new THREE.PointsMaterial({
      size: scope.size,
      side: THREE.DoubleSide,
      transparent: true
    });
    material.sizeAttenuation = false;
    if (color.length > 0) {
      material.vertexColors = true;
    } else {
      material.color.setHex(Math.random() * 0xffffff);
    }

    // build mesh

    var mesh = new THREE.Points(geometry, material);
    mesh.name = Math.random().toString();
    // var name = url.split('').reverse().join('');
    // name = /([^\/]*)/.exec(name);
    // name = name[1].split('').reverse().join('');
    // mesh.name = name;
    this.callback(material);

    return mesh;

  }

};

function findPointCloudColorby16Label(label) {
  if (label == 0) { // roadlane 车道线
    // return [64.0, 128.0, 128.0];
    return [255.0, 255.0, 255.0];
  } else if (label == 1) { // stopline 停止线
    return [255.0, 102.0, 153.0];
  } else if (label == 2) { // crosswalk 斑马线
    return [102.0, 153.0, 0.0];
  } else if (label == 3) { // roadarrow 地面箭头
    return [220.0, 200.0, 200.0];
  } else if (label == 4) {// lanemarking 地面标志及导流线禁停区域
    return [255.0, 128.0, 87.0];
  } else if (label == 5) { // guideline 车位线
    return [160.0, 255.0, 160.0];
  } else if (label == 6) { // speedbump 减速带
    return [255.0, 175.0, 240.0];
  } else if (label == 7) { // trafficsign 标志牌禁止警告指示包含
    return [51.0, 51.0, 204.0];
  } else if (label == 8) { // trafficboard 组合文字guidepost
    return [51, 51, 255];
  } else if (label == 9) { // traffic_light 红绿灯
    return [141, 238, 238];
  } else if (label == 10) { // pole 包含反光带不包含锥桶 圆形方形建筑柱子
    return [153, 255, 255];
  } else if (label == 11) { // building 建筑物以及栅栏
    return [139, 105, 20];
  } else if (label == 12) { // road 道路
    return [159, 182, 209];
  } else if (label == 13) { // sidewalk 人行道
    return [238, 230, 133];
  } else if (label == 14) { // background 树木草地天空
    return [21, 53, 0];
  } else if (label == 15) { // vehicle 车辆行人两个轮子
    return [153, 0, 153];
  } else { // other label, painted as red
    return [255.0, 0, 0];
  }
}

