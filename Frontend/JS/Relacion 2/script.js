// Ejercicio 1:
function crearTabla() {
	const container = document.querySelector("#ej1_lista")
	const tabla = document.createElement("table")
	const size = document.querySelector("#ej1_size").value

	const error = document.createTextNode("Ingrese un valor entre 1 y 7")

	if (size < 1 || size > 7) {
		container.innerHTML = ""
		container.appendChild(error)
		return ;
	}

	container.innerHTML = ""
	
	for (let i = 0; i < size; i++) {
		const filaI = document.createElement("tr")
		for (let j = 0; j < size; j++) {
			const celdaIJ = document.createElement("td")
			const texto = document.createTextNode(`  Celda ${i}${j}  `)
			celdaIJ.appendChild(texto)
			filaI.appendChild(celdaIJ)
		}
		tabla.appendChild(filaI)
		
	}
	container.appendChild(tabla)
}

const boton_ej1 = document.querySelector("#ej1_boton")
boton_ej1.addEventListener("click", crearTabla)


// Ejercicio 2:
function resetColor() {
	const semaforos = document.querySelectorAll(".semaforo")
	semaforos.forEach(semaforo => {
		semaforo.classList.remove("rojo")
		semaforo.classList.remove("amarillo")
		semaforo.classList.remove("verde")
	})
}

function ponerRojo() {
	resetColor()
	const semaforo = document.querySelectorAll(".semaforo")[0]
	semaforo.classList.add("rojo")
}

function ponerAmarillo() {
	resetColor()
	const semaforo = document.querySelectorAll(".semaforo")[1]
	semaforo.classList.add("amarillo")
}
function ponerVerde() {
	resetColor()
	const semaforo = document.querySelectorAll(".semaforo")[2]
	semaforo.classList.add("verde")
}

const boton_rojo = document.querySelector("#ej2-rojo")
const boton_amarillo = document.querySelector("#ej2-amarillo")
const boton_verde = document.querySelector("#ej2-verde")

boton_rojo.addEventListener("click", ponerRojo)
boton_amarillo.addEventListener("click", ponerAmarillo)
boton_verde.addEventListener("click", ponerVerde)


// Ejercicio 3:
const lista = document.getElementById("lista");
const boton = document.getElementById("boton");
let contador = 4;

boton.addEventListener("click", () => {
	if (contador > 10) {
		lista.removeChild(lista.firstElementChild);
	}
    const nuevoElemento = document.createElement("li");
    nuevoElemento.textContent = `Elemento ${contador}`;
    lista.appendChild(nuevoElemento);
    contador++;
});


// Ejercicio 4:
function actualizarContador() {
	const tbody = document.querySelector("#cuerpo-tabla")
	const filas = tbody.querySelectorAll("tr")
	const contador = document.querySelector("#contador")
	contador.textContent = `Número de filas: ${filas.length}`
}

function crearFila(){
	// Obtenemos los valores de los campos de texto
	const nombre = document.querySelector("#campo-nombre").value
	const apellido = document.querySelector("#campo-apellido").value
	const edad = document.querySelector("#campo-edad").value

	// Limpiamos los campos de texto
	document.querySelector("#campo-nombre").value = ""
	document.querySelector("#campo-apellido").value = ""
	document.querySelector("#campo-edad").value = ""

	// Creamos la fila y las 4 celdas
	const fila = document.createElement("tr")
	const celdaNombre = document.createElement("td")
	const celdaApellido = document.createElement("td")
	const celdaEdad = document.createElement("td")
	const celdaBotones = document.createElement("td")

	// Rellenamos las celdas con el contenido
	celdaNombre.textContent = nombre
	celdaApellido.textContent = apellido
	celdaEdad.textContent = edad
	fila.appendChild(celdaNombre)
	fila.appendChild(celdaApellido)
	fila.appendChild(celdaEdad)

	// Creamos los botones y los añadimos a la celda de botones
	const botonEditar = document.createElement("button")
	const botonEliminar = document.createElement("button")
	botonEditar.textContent = "Editar"
	botonEliminar.textContent = "Eliminar"
	celdaBotones.appendChild(botonEditar)
	celdaBotones.appendChild(botonEliminar)
	fila.appendChild(celdaBotones)

	// Añadimos la fila al tbody
	const tbody = document.querySelector("#cuerpo-tabla")
	tbody.appendChild(fila)

	botonEditar.addEventListener("click", () => {
		if (botonEditar.textContent === "Editar") {
			// Convertimos las celdas en inputs
			const textoNombre = celdaNombre.textContent
			const textoApellido = celdaApellido.textContent
			const textoEdad = celdaEdad.textContent

			celdaNombre.textContent = ""
			celdaApellido.textContent = ""
			celdaEdad.textContent = ""

			const inputNombre = document.createElement("input")
			const inputApellido = document.createElement("input")
			const inputEdad = document.createElement("input")

			inputNombre.value = textoNombre
			inputApellido.value = textoApellido
			inputEdad.value = textoEdad

			celdaNombre.appendChild(inputNombre)
			celdaApellido.appendChild(inputApellido)
			celdaEdad.appendChild(inputEdad)

			botonEditar.textContent = "Guardar"
		} else {
			// Guardamos los valores de los inputs como texto
			const inputNombre = celdaNombre.querySelector("input")
			const inputApellido = celdaApellido.querySelector("input")
			const inputEdad = celdaEdad.querySelector("input")

			celdaNombre.textContent = inputNombre.value
			celdaApellido.textContent = inputApellido.value
			celdaEdad.textContent = inputEdad.value

			botonEditar.textContent = "Editar"
		}
	})

	// Navegamos desde el botón: botón -> td -> tr -> tbody
	botonEliminar.addEventListener("click", function() {
		const fila = this.parentNode.parentNode // botón -> td -> tr
		const tbody = fila.parentNode // tr -> tbody
		tbody.removeChild(fila)
		actualizarContador() 
	})

	// Actualizamos contador después de añadir
	actualizarContador()
}

const botonAgregar = document.querySelector("#btn-añadir-fila")
botonAgregar.addEventListener("click", crearFila)