//	Ejercicio 1:
const libro = {
	autor: "Pablo",
	paginas: 225,
	disponible: true
}

const fecha = new Date()

const copia = Object.create(libro)

function imprimirCadena(nombre, objeto) {
	console.log(`--- Cadena de: ${nombre} ---`);
	let actual = objeto;
	let contador = 0;
	do {
		console.log(actual);
		actual = Object.getPrototypeOf(actual);
		contador++;
	} while (actual !== null);
	return contador;
}

//const len1 = imprimirCadena("objLiteral", libro);
// const len2 = imprimirCadena("objDate", fecha);
//const len3 = imprimirCadena("objCreate", copia);

//console.log(`Longitudes: Literal=${len1}, Date=${len2}, Create=${len3}`);


//	Ejercicio 2:
function ejercicio2() {
	const vehiculo = {
		tipo: "vehiculo",
		imprimir: () => {
			console.log(`Tipo: ${this.tipo}, Marca: ${this.marca}`);
		}
	}

	const cocheA = Object.create(vehiculo);
	cocheA.marca = "Toyota";

	const cocheB = Object.create(vehiculo);
	cocheB.marca = "Honda";

	const coches = [cocheA, cocheB];

	coches.forEach(coche => {
		console.log(`Marca '${coche.marca}':`);
		console.log("- ¿Tiene 'marca' propia?:", Object.hasOwn(coche, 'marca')); // true
		console.log("- ¿Tiene 'tipo' propia?:", Object.hasOwn(coche, 'tipo'));   // false (es heredada)
	});

	// Mostramos todas las propiedades (propias e heredadas)
	console.log("\nPropiedades con for...in (propias e heredadas):");
	for (let prop in cocheA) {
		console.log(`- ${prop}`);
	}

	console.log("\nPropiedades con Object.keys() (solo propias):");
	console.log(Object.keys(cocheA));
}

//ejercicio2();


//	Ejercicio 3:
function ejercicio3() {
	const base = {
		saludar() {
			console.log("¡Hola!");
		},
		despedirse() {
			console.log("¡Adiós!");
		}
	}

	const obj_1 = Object.create(base);
	const obj_2 = Object.create(base);
	obj_2.saludar = function () {
		console.log("¡Hola modificado v1!");
	};
	const obj_3 = Object.create(base);
	obj_3.saludar = function () {
		console.log("¡Hola modificado v2!");
	};
	obj_3.despedirse = function () {
		console.log("¡Adiós modificado v2!");
	};

	[obj_1, obj_2, obj_3].forEach((obj, index) => {
		console.log(`\nObjeto ${index + 1}:`);
		obj.saludar();
		obj.despedirse();
	});

	console.log("\nAcceso a original en objeto 3:");
	Object.getPrototypeOf(obj_3).despedirse();

}

//ejercicio3();


//	Ejercicio 4:
function ejercicio4() {
	// Sin constructor:
	const protoFigura = {
		describir() { console.log(`Figura ${this.color}, relleno: ${this.relleno}`); }
	};
	const f1 = Object.create(protoFigura); f1.color = "rojo"; f1.relleno = true;

	// Con constructor:
	function Figura(color, relleno) {
		this.color = color;
		this.relleno = relleno;
	}
	Object.assign(Figura.prototype, {
		describir() { console.log(`Figura ${this.color}, relleno: ${this.relleno}`); }
	});
	const f2 = new Figura("verde", true);

	function verificar(obj, nombre) {
		console.log(`\n--- Verificando ${nombre} ---`);
		// Propiedades de datos deben ser propias
		console.log(`¿'color' es propia?: ${Object.hasOwn(obj, 'color')}`);
		// El método NO debe ser propio, debe estar en el prototipo
		console.log(`¿'describir' es propia?: ${Object.hasOwn(obj, 'describir')}`);
	}

	verificar(f1, "f1 (Object.create)");
	verificar(f2, "f2 (Constructor)");
}

//ejercicio4();


//	Ejercicio 5:
function ejercicio5() {
	class CuentaBancaria {
		constructor(titular, saldoInicial = 0) {
			this.titular = titular;
			this.saldo = saldoInicial;
			this.movimientos = [];
		}

		ingresar(cantidad) {
			this.saldo += cantidad;
			this.movimientos.push({ tipo: "Ingreso", cantidad, saldoFinal: this.saldo });
		}

		retirar(cantidad) {
			if (cantidad > this.saldo) {
				throw new Error(`Saldo insuficiente en cuenta de ${this.titular}. Saldo actual: ${this.saldo}`);
			}
			this.saldo -= cantidad;
			this.movimientos.push({ tipo: "Retirada", cantidad, saldoFinal: this.saldo });
		}

		extracto() {
			console.log(`\n--- Extracto de ${this.titular} ---`);
			this.movimientos.forEach(m =>
				console.log(`${m.tipo}: ${m.cantidad}€ | Saldo resultante: ${m.saldoFinal}€`)
			);
		}
	}

	const c1 = new CuentaBancaria("Ana");
	const c2 = new CuentaBancaria("Luis", 100);

	// Operaciones
	c1.ingresar(50);
	c1.retirar(20);
	c2.retirar(100);

	// Mostrar extractos
	c1.extracto();
	c2.extracto();

	// Verificación de independencia
	console.log(`\nSaldo final Ana: ${c1.saldo}, Saldo final Luis: ${c2.saldo}`);
}

//ejercicio5();


//	Ejercicio 6:
function ejercicio6() {
	class Fraccion {
		constructor(numerador, denominador) {
			if (denominador === 0) throw new Error("El denominador no puede ser cero.");
			this.num = numerador;
			this.den = denominador;
		}

		#mcd(a, b) {
			return b === 0 ? Math.abs(a) : this.#mcd(b, a % b);
		}

		simplificar() {
			const divisor = this.#mcd(this.num, this.den);
			this.num /= divisor;
			this.den /= divisor;
			return this; // Permite encadenamiento
		}

		sumar(otra) {
			return new Fraccion(
				this.num * otra.den + otra.num * this.den,
				this.den * otra.den
			).simplificar();
		}

		multiplicar(otra) {
			return new Fraccion(this.num * otra.num, this.den * otra.den).simplificar();
		}

		// Sobrescritura de toString
		toString() {
			return `${this.num}/${this.den}`;
		}
	}

	// Pruebas
	const f1 = new Fraccion(1, 4);
	const f2 = new Fraccion(2, 4);

	console.log(`Fracción 1: ${f1}`); // Invoca toString automáticamente
	console.log(`Fracción 2: ${f2}`);

	const suma = f1.sumar(f2);
	console.log(`Suma (1/4 + 2/4): ${suma}`); // 3/4

	const mult = f1.multiplicar(f2);
	console.log(`Multiplicación (1/4 * 2/4): ${mult}`); // 1/8 (simplificado de 2/16)

	try {
		new Fraccion(5, 0);
	} catch (e) {
		console.error("Error capturado:", e.message);
	}
}

ejercicio6();


// Ejercicio 7:
function ejercicio7() { }

ejercicio7();


//	Ejercicio 8:
function ejercicio8() { }

ejercicio8();


//	Ejercicio 9:
function ejercicio9() { }

ejercicio9();


// Ejercicio 10:
function ejercicio10() { }

ejercicio10();


//	Ejercicio 11:
function ejercicio11() { }

ejercicio11();


//	Ejercicio 12:
function ejercicio12() { }

ejercicio12();