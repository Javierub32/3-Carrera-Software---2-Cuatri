// Ejercicio 1:
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

//iniciarSemaforo()


//	Ejercicio 2:
let contador = 10

function contadorBucle() {
	const span = document.querySelector("#span12")
	if (contador > 0) {
		span.textContent=contador
		contador--
		setTimeout(contadorBucle, 1000)
	}
	else {
		span.textContent= "TIEMPO!"
	}
}
//contadorBucle()


// Ejercicio 3:
function mostrarMensajeConRetraso(mensaje, destinatario, retrasoMs) {
  setTimeout((msg, dest) => {
    console.log(`Mensaje para ${dest}: ${msg}`);
  }, retrasoMs, mensaje, destinatario);
}

//mostrarMensajeConRetraso("Tengo jetlag, llegaré en 3s", "Ana", 3000);


// Ejercicio 4
function obtenerUsuario(id, callback) {
  setTimeout(() => {
    console.log("-> Usuario obtenido");
    callback({ id, nombre: "Ana" });
  }, Math.random() * 1000 + 500);
}

function obtenerPedidos(usuario, callback) {
  setTimeout(() => {
    console.log("-> Pedidos obtenidos");
    const pedidos = [
      { id: 1, importe: 100 },
      { id: 2, importe: 250 },
      { id: 3, importe: 50 }
    ];
    callback(pedidos);
  }, Math.random() * 1000 + 500);
}

function calcularTotal(pedidos, callback) {
  setTimeout(() => {
    console.log("-> Total calculado");
    const total = pedidos.reduce((acc, p) => acc + p.importe, 0);
    callback(total);
  }, Math.random() * 1000 + 500);
}

function mostrarResumen(total, callback) {
  setTimeout(() => {
    console.log(`El total de la compra es: $${total}`);
    callback();
  }, Math.random() * 1000 + 500);
}

/*
obtenerUsuario(42, (usuario) => {
  obtenerPedidos(usuario, (pedidos) => {
    calcularTotal(pedidos, (total) => {
      mostrarResumen(total, () => {
        console.log("Proceso finalizado.");
      });
    });
  });
});
*/


//	Ejercicio 5
function procesarResumen() { console.log("Proceso finalizado."); }

function manejarTotal(total) {
  mostrarResumen(total, procesarResumen);
}

function manejarPedidos(pedidos) {
  calcularTotal(pedidos, manejarTotal);
}

function manejarUsuario(usuario) {
  obtenerPedidos(usuario, manejarPedidos);
}

//obtenerUsuario(42, manejarUsuario);


//	Ejercicio 6:
function dividir(a, b) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (b === 0) {
                reject(new Error("División por cero"));
            } else {
                resolve(a / b);
            }
        }, 1500);
    });
}

//dividir(10, 2).then(res => console.log("Resultado:", res)).catch(err => console.error(err.message));
//dividir(10, 0).then(res => console.log("Resultado:", res)).catch(err => console.error(err.message));


// Ejercicio 7:
function ejercicio7() {
	const promesaNumeros = new Promise((resolve) => {
		setTimeout(() => resolve([1, 2, 3, 4, 5]), 300);
	});

	promesaNumeros
		.then((numeros) => {
			console.log("Original:", numeros);
			return numeros.filter(n => n % 2 === 0);
		})
		.then((pares) => {
			console.log("Pares:", pares);
			return pares.map(n => n * 10);
		})
		.then((resultado) => {
			console.log("Resultado:", resultado);
		})
		.catch((error) => {
			console.error("Error:", error);
		});
}

//ejercicio7()


//	Ejercicio 8:
function ejercicio8() {
	function carga() {
		console.log("Cargando...");
		
		return new Promise((resolve, reject) => {
			setTimeout(() => {
				const exito = Math.random() > 0.5;
				exito ? resolve("Carga correcta") : reject("Carga incorrecta");
			}, 1000);
		});
	}

	carga()
		.then((datos) => {
			console.log("Éxito:", datos);
		})
		.catch((error) => {
			console.error("Fallo:", error);
		})
		.finally(() => {
			console.log("Carga finalizada: la interfaz vuelve a estar disponible.");
		});
}

//ejercicio8()


// Ejercicio 9:
function ejercicio9() {
	// URL válida
	fetch("https://mdn.github.io/learning-area/javascript/apis/fetching-data/can-store/products.json")
		.then(response => {
			if (!response.ok) {
				throw new Error(`Error HTTP: ${response.status}`);
			}
			return response.json();
		})
		.then(productos => {
			productos.forEach(p => console.log(`Producto: ${p.name}, Precio: ${p.price}`));
		})
		.catch(err => console.error("Capturado:", err.message));

	// URL inválida
	fetch('https://pachuruchuruchue.com')
		.then(response => {
			if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
			return response.json();
		})
		.catch(err => console.error("Prueba fallida:", err.message));
}

//ejercicio9()


//	Ejercicio 10:
function ejercicio10() {
	fetch("https://mdn.github.io/learning-area/javascript/apis/fetching-data/pachuru")
		.then(response => {
			console.log(response.statusText)
			console.log(response.status)
			console.log(response.ok)
		})
		.catch(error => {
			console.error("Error al realizar la petición:", error)
		})

	fetch("https://pachurruuuu")
		.then(response => {
			console.log(response.statusText)
			console.log(response.status)
			console.log(response.ok)
		})
		.catch(error => {
			console.error("Error al realizar la petición:", error)
		})
}

//ejercicio10()


//	Ejercicio 11
function ejercicio11() {
	fetch("https://mdn.github.io/learning-area/javascript/apis/fetching-data/can-store/products.json")
		.then(response => {
				return response.json()
		})
		.then(productos => {
			const primerProducto = productos[0]
			console.log("Buscando stock para:", primerProducto.name)

			return new Promise((resolve) => {
				setTimeout(() => {
					resolve({
						producto: primerProducto.name,
						stock: Math.floor(Math.random() * 10),
					})
				}, 300)
			})
		})
		.then(infoProducto => {
			console.log("El producto", infoProducto.producto, "tiene", infoProducto.stock, "unidades disponibles")
		})
		.catch(error => {
			console.error("Error al realizar la petición:", error)
		})
}

//ejercicio11()


//	Ejercicio 12: 
function ejercicio12() {
	const urls = [
		"https://mdn.github.io/learning-area/javascript/apis/fetching-data/can-store/products.json",
		"https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json",
		"https://pachuru"
	];

	const promesas = urls.map(url => fetch(url));

	// Promise.all sirve cuando las peticiones son dependientes, por lo que si una falla, fallan todas.
	Promise.all(promesas)
		.then(respuestas => {
			respuestas.forEach(res => console.log(res.status))
		})
		.catch(error => {
			console.error("Error capturado en Promise.all:", error.message);
		});
}

//ejercicio12()


// Ejercicio 13:
function ejercicio13() {
	const servidor1 = new Promise((_, reject) => setTimeout(() => reject("Servidor 1 falló"), 800));
	const servidor2 = new Promise((resolve) => setTimeout(() => resolve("Servidor 2 respondió con éxito"), 300));
	const servidor3 = new Promise((resolve) => setTimeout(() => resolve("Servidor 3 respondió con éxito"), 1500));

	// Con Promise.all() fallaría porque uno de los servidores da error
	Promise.any([servidor1, servidor2, servidor3])
		.then(resultado => {
			console.log("Resultado de Promise.any:", resultado);
		})
		.catch(error => {
			console.error("Todas las promesas fallaron:", error);
		});
}

//ejercicio13()


// Ejercicio 14:
async function ejercicio14() {
    const urlProductos = "https://mdn.github.io/learning-area/javascript/apis/fetching-data/can-store/products.json";

    try {
        // Primera petición
        const response = await fetch(urlProductos);
        if (!response.ok) throw new Error("Error al obtener productos");
        const productos = await response.json();

        // Segunda petición (simulada)
        const primerProducto = productos[0];
        console.log(`Buscando stock para: ${primerProducto.name}`);

        const dataStock = await new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    producto: primerProducto.name,
                    unidades: Math.floor(Math.random() * 100)
                });
            }, 500);
        });

        console.log(`Producto: ${dataStock.producto} | Unidades: ${dataStock.unidades}`);
    } catch (error) {
        console.error("Error en el bloque async:", error.message);
    } finally {
        console.log("Operación finalizada (bloque finally).");
    }
}

//ejercicio14();


// Ejercicio 15:
function ejercicio15() {
	// Una función asíncrona siempre devuelve un objeto de tipo Promise
	// Si dentro de la función ocurre un error, automáticamente se rechaza esa Promise
	// El error al no tener un catch "sube" hasta la función que la invocó y así podemos manejarlo desde fuera
	async function obtenerSuperheroes() {
		const response = await fetch("https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json");
		
		if (!response.ok) {
			throw new Error(`HTTP Error: ${response.status}`);
		}
		
		const data = await response.json();
		return data.members; // Esto devuelve una promesa resuelta con el array de miembros
	}

	obtenerSuperheroes()
		.then(members => {
			members.forEach(hero => {
				console.log(`Nombre: ${hero.name}, Poderes: ${hero.powers.join(", ")}`);
			});
		})
		.catch(error => {
			console.error("Error capturado externamente:", error.message);
		});
}