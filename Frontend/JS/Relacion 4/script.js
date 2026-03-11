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

ejercicio2();


//	Ejercicio 3:
function ejercicio3() {

}

ejercicio3();


//	Ejercicio 4:
function ejercicio4() {

}

ejercicio4();


//	Ejercicio 5:
function ejercicio5() {

}

ejercicio5();


//	Ejercicio 6:
function ejercicio6() {}

ejercicio6();


// Ejercicio 7:
function ejercicio7() {}

ejercicio7();


//	Ejercicio 8:
function ejercicio8() {}

ejercicio8();


//	Ejercicio 9:
function ejercicio9() {}

ejercicio9();


// Ejercicio 10:
function ejercicio10() {}

ejercicio10();


//	Ejercicio 11:
function ejercicio11() {}

ejercicio11();


//	Ejercicio 12:
function ejercicio12() {}

ejercicio12();