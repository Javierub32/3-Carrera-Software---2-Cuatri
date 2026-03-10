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
	console.log("Semáforo en rojo.")
}

function ponerAmarillo() {
	resetColor()
	const semaforo = document.querySelectorAll(".semaforo")[1]
	semaforo.classList.add("amarillo")
	console.log("Semáforo en amarillo.")
}
function ponerVerde() {
	resetColor()
	const semaforo = document.querySelectorAll(".semaforo")[2]
	semaforo.classList.add("verde")
	console.log("Semáforo en verde.")
}

let tiempo = 0
let intervaloSemaforoID = null

function cicloSemaforo() {
	if (tiempo == 0) {
		ponerRojo()
	}
	if (tiempo == 3) {
		ponerAmarillo()
	}
	if (tiempo == 4) {
		ponerVerde()
	}
	tiempo = (tiempo + 1) % 7
}

function iniciarSemaforo() {
	if (!intervaloSemaforoID) {
		intervaloSemaforoID = setInterval(cicloSemaforo, 1000);
	}
}

document.querySelector("#ej11_reanudar").addEventListener("click", () => {
	console.log("Iniciando semáforo...")
	iniciarSemaforo()
})

document.querySelector("#ej11_detener").addEventListener("click", () => {
	clearInterval(intervaloSemaforoID)
	intervaloSemaforoID = null
	tiempo = 0
	resetColor()
	console.log("Semáforo detenido.")
})

iniciarSemaforo()

// Ejercicio 1.2:
