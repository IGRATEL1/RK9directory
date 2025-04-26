function initScene(path){
// Создание сцены
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xdddddd);

// Создание камеры
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 2, 5);

// Создание рендерера
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Добавление освещения
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(10, 10, 10);
scene.add(directionalLight);

// Загрузка модели
const loader = new THREE.GLTFLoader();
let model;

loader.load(
    path, // Укажите правильный путь к файлу
    function (gltf) {
        model = gltf.scene;
        scene.add(model);
        
        // Масштабирование модели при необходимости
        model.scale.set(1, 1, 1);
        
        // Позиционирование модели
        model.position.set(0, 0, 0);
    },
    undefined,
    function (error) {
        console.error(error);
    }
);

// Добавление OrbitControls
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Обработчик изменения размера окна
window.addEventListener('resize', onWindowResize, false);

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Анимация
function animate() {
    requestAnimationFrame(animate);

    // Вращение модели
    if (model) {
        model.rotation.y += 0.005;
    }

    controls.update();
    renderer.render(scene, camera);
}

animate();
}