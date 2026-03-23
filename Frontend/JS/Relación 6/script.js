// Ejercicio 1:
let tema = localStorage.getItem("tema") || "claro";

const actualizarPreferencias = () => {
	body = document.querySelector("body");
	if (tema == "oscuro") {
		body.style.backgroundColor = "black";
		body.style.color = "white";
	} else {
		body.style.backgroundColor = "white";
		body.style.color = "black";
	}
	localStorage.setItem("tema", tema);
};

document.querySelector("#ej1-tema").addEventListener("click", function () {
	tema = tema == "oscuro" ? "claro" : "oscuro";
	actualizarPreferencias();
});

actualizarPreferencias();

// Ejercicio 2:
const botones = document.querySelectorAll(".btn-carrito");
let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

const actualizarBotones = () => {
	botones.forEach((boton) => {
		const producto = boton.parentElement.querySelector("h3").innerText;

		if (carrito.includes(producto)) {
			boton.innerText = "Michi comprado";
		} else {
			boton.innerText = "Comprar michi";
		}
	});

	localStorage.setItem("carrito", JSON.stringify(carrito));
};

botones.forEach((boton) => {
	boton.addEventListener('click', () => {
		const producto = boton.parentElement.querySelector("h3").innerText;

		if (carrito.includes(producto)) {
			carrito = carrito.filter((item) => item !== producto);
		} else {
			carrito.push(producto);
		}

		actualizarBotones();
	});
});

actualizarBotones();


// Ejercicio 3:
const peticionApertura = window.indexedDB.open("bd_notas", 2);
let bd;

peticionApertura.addEventListener("error", () => console.log("Error al abrir la BD"));

peticionApertura.addEventListener("success", () => {
	console.log("Acceso a BD correcto");
	bd = peticionApertura.result;
	mostrarNotas();
});

peticionApertura.addEventListener("upgradeneeded", () => {
	console.log("Creando la BD");
	bd = peticionApertura.result;
	const objectStore = bd.createObjectStore("notas", { keyPath: "id", autoIncrement: true });
	objectStore.createIndex("titulo", "titulo", { unique: false });
	objectStore.createIndex("contenido", "contenido", { unique: false });

	console.log("BD creada");
});

function añadirNota() {
	const titulo = document.querySelector("#ej3-titulo").value;
	const contenido = document.querySelector("#ej3-descripcion").value;
	const transaccion = bd.transaction(["notas"], "readwrite");
	const objectStore = transaccion.objectStore("notas");
	objectStore.add({ titulo, contenido });

	transaccion.addEventListener("complete", () => {
		console.log("Nota añadida correctamente");
		document.querySelector("#ej3-titulo").value = "";
		document.querySelector("#ej3-descripcion").value = "";
	});

	transaccion.addEventListener("error", () => console.log("Error al añadir la nota"));

	mostrarNotas();
}

document.querySelector("#ej3-guardar").addEventListener("click", añadirNota);

function mostrarNotas() {
	const transaccion = bd.transaction(["notas"], "readonly");
	const objectStore = transaccion.objectStore("notas");
	const peticion = objectStore.getAll();

	peticion.addEventListener("success", () => {
		const notas = peticion.result;
		const contenedor = document.querySelector("#ej3-notas");
		contenedor.innerHTML = "";
		notas.forEach((nota) => {
			const divNota = document.createElement("div");
			divNota.innerHTML = `<h3>${nota.titulo}</h3><p>${nota.contenido}</p>`;
			contenedor.appendChild(divNota);
		});
	});

	peticion.addEventListener("error", () => console.log("Error al obtener las notas"));
}