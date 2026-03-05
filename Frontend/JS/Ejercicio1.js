// Ejercicio 1:
// typeof(null) es un objeto porque el marcador de un objeto es 000 y como null es un puntero nulo, acaba teniendo ese marcador, no lo han arreglado por retrocompatibilidad.
let num;
num = 7;
console.log(typeof(num));
num = "hola";
console.log(typeof(num));
num = true;
console.log(typeof(num));
num = null;
console.log(typeof(num));


// Ejercicio 2:
// JavaScript crea momentaneamente un objeto de tipo Number que tiene estas funciones y luego lo vuelve a poner como dato primitivo.
let pi = 3.13159
console.log(pi.toString());
console.log(pi.toFixed(2));
console.log(pi.toExponential());


// Ejercicio 3:
// Si intentaramos reasignar el valor de libro da error por ser constante.
const libro = {
  titulo: "Titulo",
  autor:"Autor",
  paginas: 229,
};

console.log("Libro sin modificar", libro)
libro.paginas = 500;
libro.editorial = "Editorial";
console.log("Después de editar", libro)


// Ejercicio 4:
// || devuelve el otro si el primero es falsy (null, undefined, 0, "", false, NaN)
// ?? devuelve el otro si el primero es nullish (null, undefined)
let var1 = null;
let var2 = undefined;
let var3 = 0;
let var4 = "";

console.log(var1 ?? "Soy nullish")
console.log(var2 ?? "Soy nullish")
console.log(var3 ?? "Hola")
console.log(var4 ?? "Hola")


// Ejercicio 5:
let num1 = 10;
let num2 = 3;

console.log(`Suma (10 + 3): ${num1 + num2}`);
console.log(`Resta (10 - 3): ${num1 - num2}`);
console.log(`Producto (10 * 3): ${num1 * num2}`);
console.log(`División (10 / 3): ${num1 / num2}`);
console.log(`Resto (10 % 3): ${num1 % num2}`);
console.log(`Exponenciación (10 ** 3): ${num1 **num2}`);

let n = 5;
let str = '5';

// El operador débil (==) hace una conversión de tipos
// E operador fuerte (===) no
console.log(`¿n == str?  : ${n == str}`);  // true
console.log(`¿n === str? : ${n === str}`); // false
console.log(`¿n != str?  : ${n != str}`);  // false
console.log(`¿n !== str? : ${n !== str}`); // true


// Ejercicio 6:
const clasificarNota = (nota) => {
    return nota < 5 ? "Suspenso" 
         : nota < 7 ? "Aprobado" 
         : nota < 9 ? "Notable" 
         : "Sobresaliente";
};

console.log(`Nota 4: ${clasificarNota(4)}`);
console.log(`Nota 6.5: ${clasificarNota(6.5)}`);
console.log(`Nota 8: ${clasificarNota(8)}`);
console.log(`Nota 9.5: ${clasificarNota(9.5)}`);
console.log(`Nota 10: ${clasificarNota(10)}`);


// Ejercicio 7:
// 'in' comprueba los ÍNDICES, no los valores.
// Si quiero buscar un valor tengo que usar frutas.includes("Manzana")
const vehiculo = {
    marca: "Toyota",
    modelo: "Corolla",
    año: 2023
};

console.log(`¿Tiene 'marca'?: ${"marca" in vehiculo}`);   // true
console.log(`¿Tiene 'color'?: ${"color" in vehiculo}`);   // false
console.log(`¿Tiene 'length'?: ${"length" in vehiculo}`); // false

const frutass = ["Manzana", "Pera", "Plátano", "Uva", "Cereza"];

console.log(`¿Existe índice 0?: ${0 in frutass}`);       // true
console.log(`¿Existe índice 4?: ${4 in frutass}`);       // true
console.log(`¿Existe índice 7?: ${7 in frutass}`);       // false
console.log(`¿Tiene propiedad 'length'?: ${"length" in frutass}`); // true


// Ejercicio 8:
const cadena = "Desarrollo de Aplicaciones Web";

console.log(`Longitud: ${cadena.length}`);
console.log(`Carácter en posición 11: ${cadena.charAt(11)}`); 
console.log(`¿Contiene 'Web'?: ${cadena.includes("Web")}`);
console.log(`¿Empieza por 'Desa'?: ${cadena.startsWith("Desa")}`);
console.log(`¿Termina en 'web' (minúsculas)?: ${cadena.endsWith("web")}`); 
console.log(`Posición de la primera 'a': ${cadena.indexOf("a")}`);
console.log(`Subcadena desde posición 12 al final: ${cadena.slice(12)}`);


// Ejercicio 9:
const frase = "la programación en javascript es divertida";

console.log(frase.toUpperCase());

const titulo = frase
    .split(" ")
    .map(word => word[0].toUpperCase() + word.slice(1))
    .join(" ");
console.log(titulo);

const fraseArroba = frase.replaceAll("a", "@");
console.log(fraseArroba);
console.log(`Longitud resultante: ${fraseArroba.length}`);


// Ejercicio 10:
const producto = {
    nombre: "Teclado Mecánico",
    precio: 85.50,
    cantidad: 3
};

console.log(`Producto: ${producto.nombre}
Precio unitario: ${producto.precio}€
Total: ${(producto.precio * producto.cantidad).toFixed(2)}€
Estado stock: ${producto.cantidad < 5 ? "¡ATENCIÓN: Stock bajo!" : "Stock suficiente"}`);


// Ejercicio 11:
const poema = `Verso1
verso2 más guapo
verso3 me gusta el pan`;

console.log(poema);

const versos = poema.split("\n");
console.log(`Número de versos: ${versos.length}`);

const unaLinea = versos.join(" / ")
console.log(unaLinea);


// Ejercicio 12:
let frutas = ["Manzana", "Pera", "Plátano", "Uva", "Cereza"];
console.log("Array inicial:", frutas);

// Añade una fruta al final (push)
let push = frutas.push("Kiwi");
console.log(`Tras push: [${frutas}] | Valor devuelto (longitud): ${push}`);

// Borra la fruta del final (pop)
let pop = frutas.pop();
console.log(`Tras Pop: [${frutas}] | Valor devuelto (eliminado): ${pop}`);

// Elimina la primera fruta (shift)
let shift = frutas.shift();
console.log(`Tras shift: [${frutas}] | Valor devuelto (eliminado): ${shift}`);

// Añade dos frutas al principio (unshift)
let unshift = frutas.unshift("Mango", "Naranja");
console.log(`Tras unshift: [${frutas}] | Valor devuelto (longitud): ${unshift}`);

// Elimina la/las frutas de la posición 3 en adelante las que se pidan splice(índice, cuántos eliminar)
let rSplice = frutas.splice(3, 2);
console.log(`Tras splice(3,2): [${frutas}] | Valor devuelto (array eliminados): [${rSplice}]`);


// Ejercicio 13:
const numerosBusqueda = [10, 20, 30, 20, 40, 20, 50];

const analizarValor = (arr, valor) => {
    console.log(`¿Está incluido?: ${arr.includes(valor)}`);
    console.log(`Primera aparición (indexOf): ${arr.indexOf(valor)}`);
    console.log(`Última aparición (lastIndexOf): ${arr.lastIndexOf(valor)}`);
    
    const apariciones = arr.filter(n => n === valor).length;
    console.log(`Número de apariciones: ${apariciones}`);
};

analizarValor(numerosBusqueda, 20);
analizarValor(numerosBusqueda, 99);


// Ejercicio 14:
const pares = [2, 4, 6, 8, 10];
const impares = [1, 3, 5, 7, 9];

const todos = pares.concat(impares);
console.log("Array concatenado:", todos);
console.log("Con toString():", todos.toString());
console.log("Con join(' - '):", todos.join(" - "));
console.log("Longitud total:", todos.length);


// Ejercicio 15:
const dias = ["lunes", "martes", "miércoles", "jueves", "viernes"];

for (let i = 0; i < dias.length; i++) {
    console.log(`Índice ${i}: ${dias[i]}`);
}

for (const dia of dias) {
    console.log(dia.toUpperCase());
}

dias.forEach(dia => {
    console.log(`${dia} (longitud: ${dia.length})`);
});


// Ejercicio 16:
const numeros = [3, 7, 2, 9, 4, 11, 6, 8, 1, 5];

const cuadrados = numeros.map(n => n ** 2);
console.log("Cuadrados:", cuadrados);

const mayoresCinco = numeros.filter(n => n > 5);
console.log("Mayores que 5:", mayoresCinco);

const cuadradosDeMayores = numeros
    .filter(n => n > 5)
    .map(n => n ** 2);
console.log("Cuadrados de los que son > 5:", cuadradosDeMayores);


// Ejercicio 17:
function imc(peso, altura, unidad = "métrico") {
    let p = peso;
    let a = altura;

    if (unidad === "imperial") {
        p = peso * 0.453592;
        a = altura * 0.0254;
    }

    const resultado = p / (a ** 2);
    return resultado.toFixed(2);
}

console.log(`Métrico (defecto): ${imc(80, 1.80)}`); 
console.log(`Imperial: ${imc(176, 70, "imperial")}`);


// Ejercicio 18:
const datos = [4, 8, 15, 16, 23, 42];

function mediaDeclarada(arr) {
    let suma = arr.reduce((acum, num) => acum + num, 0);
    return suma / arr.length;
}

const mediaExpresion = function(arr) {
    let suma = arr.reduce((acum, num) => acum + num, 0);
    return suma / arr.length;
};

const mediaFlecha = (arr) => arr.reduce((a, b) => a + b, 0) / arr.length;

console.log("Declarada:", mediaDeclarada(datos));
console.log("Expresión:", mediaExpresion(datos));
console.log("Flecha:", mediaFlecha(datos));


// Ejercicio 19:
const nombres = ["Ana", "Carlos", "Beatriz", "David", "Elena"];

const longitudes = nombres.map(n => n.length);
console.log(nombres)
console.log("Longitudes:", longitudes);

const largos = nombres.filter(n => n.length > 5);
console.log("Más de 5 letras:", largos);

const saludos = nombres.map(n => `Hola, ${n}!`);
console.log(saludos);


// Ejercicio 21:
