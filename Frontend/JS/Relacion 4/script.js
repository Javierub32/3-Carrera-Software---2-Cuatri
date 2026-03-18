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

//ejercicio6();


// Ejercicio 7:
function ejercicio7() {
	class Figura {
		color;
		figura = "figura";

		constructor(color, figura) {
			this.color = color;
			this.figura = figura;
		}

		describir() {
			console.log(this.figura, "de color", this.color);
		}

		area() {
			throw new Error("área no implementada")
		}
	}

	class Circulo extends Figura {
		radio;

		constructor(color, radio) {
			super(color, "Circulo")
			this.radio = radio
		}

		describir() {
			super.describir();
			console.log("Radio:", this.radio);
		}

		area() {
			return Math.PI * (this.radio * this.radio);
		}
	}

	class Rectangulo extends Figura {
		base;
		altura;

		constructor(color, base, altura) {
			super(color, "Rectangulo");
			this.base = base;
			this.altura = altura;
		}

		describir() {
			super.describir();
			console.log(`Base: ${this.base}, Altura: ${this.altura}`);
		}

		area() {
			return this.base * this.altura;
		}
	}

	class Triangulo extends Figura {
		base;
		altura;

		constructor(color, base, altura) {
			super(color, "Triangulo");
			this.base = base;
			this.altura = altura;
		}

		describir() {
			super.describir();
			console.log(`Base: ${this.base}, Altura: ${this.altura}`);
		}

		area() {
			return (this.base * this.altura) / 2;
		}
	}

	// Uso
	const figuras = [
		new Circulo("Rojo", 5),
		new Rectangulo("Azul", 10, 5),
		new Triangulo("Verde", 8, 4)
	];

	let areaTotal = 0;
	figuras.forEach(f => {
		f.describir();
		areaTotal += f.area();
		console.log(`Área: ${f.area().toFixed(2)}\n`);
	});

	console.log(`Área total de todas las figuras: ${areaTotal.toFixed(2)}`);
}

//ejercicio7();


//	Ejercicio 8:
function ejercicio8() {
	class Empleado {
		nombre;
		salario;

		constructor(nombre, salario) {
			this.nombre = nombre;
			this.salario = salario;
		}

		presentacion() {
			return `Empleado: ${this.nombre}, Salario: ${this.salario}`;
		}
	}

	class Gestor extends Empleado {
		departamento;

		constructor(nombre, salario, departamento) {
			super(nombre, salario);
			this.departamento = departamento;
			this.equipo = [];
		}

		presentacion() {
			return `${super.presentacion()}, Departamento: ${this.departamento}, Equipo: ${this.equipo.length} personas`;
		}
	}

	class Director extends Gestor {
		presupuesto;

		constructor(nombre, salario, departamento, presupuesto) {
			super(nombre, salario, departamento);
			this.presupuesto = presupuesto;
		}

		presentacion() {
			return `${super.presentacion()}, Presupuesto: ${this.presupuesto}`;
		}
	}

	// Instancias
	const emp = new Empleado("Ana", 30000);
	const gest = new Gestor("Luis", 50000, "Ventas");
	const dir = new Director("Marta", 80000, "Dirección General", 1000000);

	gest.equipo.push(emp);

	console.log(emp.presentacion());
	console.log(gest.presentacion());
	console.log(dir.presentacion());

	console.log("\n");

	console.log("¿Director es Director?:", dir instanceof Director); // true
	console.log("¿Director es Gestor?:", dir instanceof Gestor);     // true
	console.log("¿Director es Empleado?:", dir instanceof Empleado); // true
	console.log("¿Gestor es Empleado?:", gest instanceof Empleado);   // true
}

//ejercicio8();


//	Ejercicio 9:
function ejercicio9() {
	class Temperatura {
		#celsius;

		constructor(celsius) {
			this.celsius = celsius;
		}

		get celsius() {
			return this.#celsius;
		}

		set celsius(valor) {
			if (valor < -273.15) {
				throw new Error("La temperatura no puede ser inferior al cero absoluto (-273.15 °C)");
			}
			this.#celsius = valor;
		}

		get fahrenheit() {
			return (this.#celsius * 9) / 5 + 32;
		}

		get kelvin() {
			return this.#celsius + 273.15;
		}
	}

	const temp1 = new Temperatura(25);
	console.log(`Temp1: ${temp1.celsius}°C, ${temp1.fahrenheit}°F, ${temp1.kelvin}K`);

	temp1.celsius = 0; // Accede al setter de forma automática
	console.log(`Temp1 actualizada: ${temp1.celsius}°C, ${temp1.fahrenheit}°F, ${temp1.kelvin}K`);

	try {
		temp1.celsius = -300; // Esto debería lanzar un error
	} catch (e) {
		console.error("Error capturado:", e.message);
	}

	// Verificamos la encapsulacion
	// console.log(temp1.#celsius); // -> Esto produce un SyntaxError
}

//ejercicio9();


// Ejercicio 10:
function ejercicio10() {
	class Contrasena {
		#hash;

		constructor(texto) {
			this.#hash = this.#calcularHash(texto);
		}

		#calcularHash(texto) {
			let suma = 0;
			for (let i = 0; i < texto.length; i++) {
				suma += texto.charCodeAt(i);
			}
			return suma.toString(16); // Representación hexadecimal
		}

		verificar(texto) {
			return this.#calcularHash(texto) === this.#hash;
		}

		mostrarHash() {
			return this.#hash;
		}
	}

	const psw = new Contrasena("contrasena");

	console.log("Hash generado:", psw.mostrarHash());
	console.log("¿Es 'contrasena' la contraseña?:", psw.verificar("contrasena")); // true
	console.log("¿Es '123' la contraseña?:", psw.verificar("12345"));           // false
}

//ejercicio10();


//	Ejercicio 11:
function ejercicio11() {
	class Producto {
		static #contador = 0; // Propiedad estática privada compartida

		constructor(nombre, precio) {
			Producto.#contador++;
			this.id = Producto.#contador;
			this.nombre = nombre;
			this.precio = precio;
		}

		static crearConDescuento(nombre, precio, porcentaje) {
			const precioFinal = precio - (precio * porcentaje / 100);
			return new Producto(nombre, precioFinal);
		}

		static totalCreados() {
			return Producto.#contador;
		}
	}

	const p1 = new Producto("Laptop", 1000);
	const p2 = Producto.crearConDescuento("Mouse", 50, 10);

	console.log(`Producto 1: ${p1.nombre}, ID: ${p1.id}, Precio: ${p1.precio}`);
	console.log(`Producto 2: ${p2.nombre}, ID: ${p2.id}, Precio: ${p2.precio}`);
	console.log(`Total de productos creados: ${Producto.totalCreados()}`); // Debe ser 2
}

//ejercicio11();


//	Ejercicio 12:
function ejercicio12() {
	class Validador {
		static VERSION = "1.0";

		constructor() {
			throw new Error("La clase Validador es una clase utilitaria y no debe ser instanciada.");
		}

		static esEmail(texto) {
			const partes = texto.split("@");
			return partes.length === 2 && partes[1].includes(".");
		}

		static esContrasenaFuerte(texto) {
			const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
			return regex.test(texto);
		}

		static esEnteroPositivo(valor) {
			return Number.isInteger(valor) && valor > 0;
		}

		static esFecha(texto) {
			const regex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
			const match = texto.match(regex);
			if (!match) return false;

			const [_, d, m, a] = match.map(Number);
			const fecha = new Date(a, m - 1, d);

			return fecha.getFullYear() === a && fecha.getMonth() === m - 1 && fecha.getDate() === d;
		}
	}

	console.log("Email (validar@test.com):", Validador.esEmail("validar@test.com")); // true
	console.log("Email (invalido):", Validador.esEmail("invalido@com")); // false

	console.log("Contraseña (Pass1234):", Validador.esContrasenaFuerte("Pass1234")); // true
	console.log("Contraseña (corta):", Validador.esContrasenaFuerte("Ab1")); // false

	console.log("Entero (10):", Validador.esEnteroPositivo(10)); // true
	console.log("Entero (-5):", Validador.esEnteroPositivo(-5)); // false

	console.log("Fecha (31/01/2024):", Validador.esFecha("31/01/2024")); // true
	console.log("Fecha (31/02/2024):", Validador.esFecha("31/02/2024")); // false (no existe)

	// Verificación de error al instanciar
	try {
		new Validador();
	} catch (e) {
		console.log("\nError:", e.message);
	}
}

ejercicio12();