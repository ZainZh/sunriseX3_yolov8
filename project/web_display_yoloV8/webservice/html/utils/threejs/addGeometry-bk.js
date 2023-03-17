import Line from './shader/index';
import BasicShader from './shader/basic';

export default class ThreeGeometry {
  constructor(group, laneMarkings, renderer, scene, camera) {
    this.group = group;
    this.laneMarkings=laneMarkings;
    this.renderer = renderer;
    this.scene = scene;
    this.camera = camera;
    this.materials = [];
  }

  /**重绘场景 */
  renderGL() {
    this.renderer.render(this.scene, this.camera);
  }

  /**添加圆柱 */
  addCylinder({center = [0, 0, 0], radius = 1, height = 1, color = 0xffffff, order = 1} = {}) {
    let geometry = new THREE.CylinderBufferGeometry(radius, radius, height);
    let material = new THREE.MeshLambertMaterial({
      color,
      depthTest: false,
      transparent:true
    });
    let cylinder = new THREE.Mesh(geometry, material);
    // cylinder.position.copy(new THREE.Vector3((datas.points[0].x + datas.points[1].x) / 2, (datas.points[0].z + datas.points[1].z) / 2, -(datas.points[0].y + datas.points[1].y) / 2));
    cylinder.position.copy(new THREE.Vector3(...center));
    cylinder.renderOrder = order;
    this.group.add(cylinder);
    this.renderGL();
    this.materials.push(material);
  }

  /**添加折线 */
  addPolyLine({points = [], predPoints = [], succPoints = [], color = 0xffffff, width = 1, opacity = 1, order = 1} = {}) {
    let mat;
    let lineGeometry;
    let mesh;

    //有控制点数据则生成三次贝塞尔曲线（取曲线上的30个点）
    if (predPoints.length > 0 && succPoints.length > 0) {
      let vertices = [];
      points.map((point, index) => {
        if (index < points.length - 1) {
          var curve = new THREE.CubicBezierCurve3(
            new THREE.Vector3(point.x, point.y, point.z),
            new THREE.Vector3(succPoints[index].x, succPoints[index].y, succPoints[index].z),
            new THREE.Vector3(predPoints[index + 1].x, predPoints[index + 1].y, predPoints[index + 1].z),
            new THREE.Vector3(points[index + 1].x, points[index + 1].y, points[index + 1].z)
          );
          vertices.push(...curve.getPoints(30));
        }
        points = vertices;
      });
    }

    //width大于0则使用shader生成带宽度的线（单位为米），等于0则使用LineBasicMaterial（宽度为1px）
    if (width > 0) {
      mat = new THREE.ShaderMaterial(BasicShader(THREE)({
        side: THREE.DoubleSide,
        diffuse: color,
        thickness: width,
        opacity
      }));
      let vertices = [];
      points.map(point => {
        vertices.push([point.x, point.y, point.z]);
      });
      lineGeometry = Line(THREE)(vertices, {distances: true, closed: false});
      mesh = new THREE.Mesh(lineGeometry, mat);
      mesh.rotateX(-Math.PI / 2);
    } else {
      mat = new THREE.LineBasicMaterial({
        color,
        shading: THREE.SmoothShading,
        depthTest: false
      });
      lineGeometry = new THREE.Geometry();
      points.map(point => {
        lineGeometry.vertices.push(new THREE.Vector3(point.x, point.z, -point.y));
      });
      mesh = new THREE.Line(lineGeometry, mat);
    }
    mesh.renderOrder = order;
    // console.log(mesh, 'ms');
    this.group.add(mesh);
    this.renderGL();
    this.materials.push(mat);
  }

  /**添加多边形 */
  addPolygon({points = [], color = 0xffffff, opacity = 1, order = 1} = {}) {
    let geometry = new THREE.Geometry();
    points.map((point, index) => {
      geometry.vertices.push(new THREE.Vector3(point.x, point.z, -point.y));
      if (index < points.length - 2) {
        geometry.faces.push(new THREE.Face3(0, index + 1, index + 2));
      }
    });
    let material = new THREE.MeshBasicMaterial({
      color,
      side: THREE.DoubleSide,
      transparent: true,
      opacity,
      depthTest: false
    });
    let mesh = new THREE.Mesh(geometry, material);
    mesh.renderOrder = order;
    this.group.add(mesh);
    this.renderGL();

    this.materials.push(material)
  }

  shapeGeometry({points = [], color = 0xffffff, opacity = 1, order = 1} = {}) {
    let shape = new THREE.Shape();
    let positionZ=0;
    points.map((point, index) => {
      if(index===0){
        shape.moveTo(points[0].x, points[0].y);
      }
      shape.lineTo(point.x, point.y);
      positionZ=point.z
    });
    shape.lineTo(points[0].x, points[0].y);
    let geometry=new THREE.ShapeGeometry(shape);
    let material=new THREE.MeshBasicMaterial({
      color,
      side: THREE.DoubleSide,
      transparent: true,
      opacity,
      depthTest: false
    });
    let mesh=new THREE.Mesh(geometry,material);
    mesh.renderOrder=order;
    mesh.position.z=positionZ;
    this.laneMarkings.add(mesh);
    this.group.add(this.laneMarkings);
    this.renderGL();

    this.materials.push(material);
  }

  /**添加带材质的多边形 */
  addTexturePolygon({textureURL = '', points = [], opacity = 1, order = 1} = {}) {
    if (textureURL === '') {
      return;
    }

    let texture = new THREE.TextureLoader().load(textureURL, () => {
      texture.wrapS = THREE.RepeatWrapping;
      texture.wrapT = THREE.RepeatWrapping;
      texture.repeat.set(1, 1);
      let geometry = new THREE.Geometry();
      points.map((point, index) => {
        geometry.vertices.push(new THREE.Vector3(point.x, point.z, -point.y));
        if (index < points.length - 2) {
          geometry.faces.push(new THREE.Face3(0, index + 1, index + 2));
        }
      });
      geometry.computeBoundingBox();
      let max = geometry.boundingBox.max;
      let min = geometry.boundingBox.min;

      let offset = new THREE.Vector2(0 - min.x, 0 - min.y);
      let range = new THREE.Vector2(max.x - min.x, max.y);
      let faces = geometry.faces;
      geometry.faceVertexUvs[0] = [];

      for (let i = 0; i < faces.length; i++) {
        let v1 = geometry.vertices[faces[i].a];
        let v2 = geometry.vertices[faces[i].b];
        let v3 = geometry.vertices[faces[i].c];
        geometry.faceVertexUvs[0].push([
          new THREE.Vector2((v1.x + offset.x) / range.x, (v1.y + offset.y) / range.y),
          new THREE.Vector2((v2.x + offset.x) / range.x, (v2.y + offset.y) / range.y),
          new THREE.Vector2((v3.x + offset.x) / range.x, (v3.y + offset.y) / range.y)
        ]);
      }

      geometry.uvsNeedUpdate = true;

      let material = new THREE.MeshBasicMaterial({
        side: THREE.DoubleSide,
        transparent: true,
        opacity,
        depthTest: false,
        map: texture
      });
      let mesh = new THREE.Mesh(geometry, material);
      mesh.renderOrder = order;
      this.group.add(mesh);
      this.renderGL();
      this.materials.push(material)
    });
  }

  /**获取全部材质 */
  getMaterials() {
    return this.materials;
  }
}
