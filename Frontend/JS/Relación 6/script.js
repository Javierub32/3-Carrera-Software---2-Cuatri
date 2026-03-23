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

const añadirNota = () => {
	const titulo = document.querySelector("#ej3-titulo").value;
	const contenido = document.querySelector("#ej3-descripcion").value;
	const transaccion = bd.transaction(["notas"], "readwrite");
	const objectStore = transaccion.objectStore("notas");
	titulo && contenido ? objectStore.add({ titulo, contenido }) : console.log("Título y descripción son obligatorios");

	transaccion.addEventListener("complete", () => {
		document.querySelector("#ej3-titulo").value = "";
		document.querySelector("#ej3-descripcion").value = "";
		mostrarNotas(); // Si lo pones fuera puede petar
	});

	transaccion.addEventListener("error", () => console.log("Error al añadir la nota"));
}

const mostrarNotas = () => {
	const transaccion = bd.transaction(["notas"], "readonly");
	const objectStore = transaccion.objectStore("notas");
	const peticion = objectStore.getAll();

	peticion.addEventListener("success", () => {
		const notas = peticion.result;
		const contenedor = document.querySelector("#ej3-notas");
		contenedor.innerHTML = "";
		notas.forEach((nota) => {
			const divNota = document.createElement("div");
			divNota.innerHTML = `
				<h3>${nota.titulo}</h3>
				<p>${nota.contenido}</p>
				<button class="btn-borrar" id=${nota.id}>Eliminar</button>`;
			contenedor.appendChild(divNota);
		});
	});

	peticion.addEventListener("error", () => console.log("Error al obtener las notas"));
}

const eliminarNota = (id) => {
	const transaccion = bd.transaction(["notas"], "readwrite");
	const objectStore = transaccion.objectStore("notas");
	objectStore.delete(id);

	transaccion.addEventListener("complete", () => {
		mostrarNotas();
	});
}

peticionApertura.addEventListener("error", () => console.log("Error al abrir la BD"));

peticionApertura.addEventListener("success", () => {
	//console.log("Acceso a BD correcto");
	bd = peticionApertura.result;
	mostrarNotas();
});

peticionApertura.addEventListener("upgradeneeded", () => {
	//console.log("Creando la BD");
	bd = peticionApertura.result;
	const objectStore = bd.createObjectStore("notas", { keyPath: "id", autoIncrement: true });
	objectStore.createIndex("titulo", "titulo", { unique: false });
	objectStore.createIndex("contenido", "contenido", { unique: false });
	//console.log("BD creada");
});

document.querySelector("#ej3-guardar").addEventListener("click", añadirNota);

document.querySelector("#ej3-notas").addEventListener("click", (e) => {
	if (e.target.classList.contains("btn-borrar")) {
		const id = Number(e.target.id);
		eliminarNota(id);
	}
})


// Ejercicio 4:
const imageFolder = "michiss";
const imageUrl = "https://imgs.search.brave.com/qMAoWcazmnjOvSDp4ckEQsmd8a_KB4skOHc2K7E-sJs/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTM3/Mzg1Mzc0L2VzL2Zv/dG8vc3VycHJpc2Vk/LWNhdC5qcGc_cz02/MTJ4NjEyJnc9MCZr/PTIwJmM9dGRqZ1lX/OWRVY3NVNmswTm1S/d25NbWo2cldYUFZt/M01VbEVDWnJ1NndN/MD0";
const imageId = "michi"

const imageStatus = document.querySelector("#ej4-status");

const openRequest_ej4 = window.indexedDB.open("ej4-image", 5);
let bd_ej4;

// Hacemos los casos de éxito, error y actualización de la base de datos
openRequest_ej4.addEventListener("success", () => {
	console.log("Conectado a DB-ej4");
	bd_ej4 = openRequest_ej4.result;
	loadImage();
})

openRequest_ej4.addEventListener("upgradeneeded", () => {
	console.log("Creando DB-ej4");
	bd_ej4 = openRequest_ej4.result;
    if (!bd_ej4.objectStoreNames.contains(imageFolder)) {
        bd_ej4.createObjectStore(imageFolder);
    }
})

openRequest_ej4.addEventListener("error", () => console.log("Error al abrir la BD"));

// Función para cargar la imagen
async function loadImage() {
	const transaction = bd_ej4.transaction([imageFolder], "readwrite"); // Pido permisos para entrar
	const objectStore = transaction.objectStore(imageFolder); 			// Entro
	const request = objectStore.get(imageId); 							// Pido la imagen

	request.addEventListener("success", async () => {
		console.log("Request a imagen completada");
		if (request.result) {
			console.log("Imagen cargada desde DB");
			imageStatus.innerText = "Imagen cargada desde DB";
			mostrarImagen(request.result);
		} else {
			console.log("Imagen cargada desde Red");
			imageStatus.innerText = "Cargando imagen desde Red";
			try {
				const response = await fetch(imageUrl);
				const blob = await response.blob();

				saveBlobAtDB(blob);
				mostrarImagen(blob);

				imageStatus.innerText = "Imagen cargada desde red";
			} catch {
				console.log("Error cargando la imagen");
			}
		}
	})

	transaction.addEventListener("complete", () => {
		console.log("Transaccion acabada, mostramos imagen");
		
	})
}

function mostrarImagen(blob) {
    const contenedor = document.querySelector("#contenedor-michi");

    const urlImagen = URL.createObjectURL(blob);
    
    const img = document.createElement("img");
    img.src = urlImagen;
    img.style.width = "300px";
    img.style.borderRadius = "10px";
    
    contenedor.innerHTML = "";
    contenedor.appendChild(img);
}

function saveBlobAtDB(blob) {
	const transaction = bd_ej4.transaction([imageFolder], "readwrite");
	const objectStore = transaction.objectStore(imageFolder);
	const request = objectStore.put(blob, imageId);

	request.addEventListener("success", () => console.log("Imagen guardada correctamente"));
	transaction.addEventListener("complete", () => console.log("Cerramos transacción de guardar imagen")); 
}



