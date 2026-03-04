// Ejercicio 1:
// typeof(null) es un objeto porque el marcador de un objeto es 000 y como null es un puntero nulo, acaba teniendo ese marcador, no lo han arreglado por retrocompatibilidad.
let num;
num = 7;
console.log(typeof(num))
num = "hola";
console.log(typeof(num))
num = true;
console.log(typeof(num))
num = null;
console.log(typeof(num))


// Ejercicio 2:
// JavaScript crea momentaneamente un objeto de tipo Number que tiene estas funciones y luego lo vuelve a poner como dato primitivo.
let pi = 3.13159
console.log(pi.toString())
console.log(pi.toFixed(2))
console.log(pi.toExponential())

// Ejercicio 3:


