// Ejercicio 1:
const cargarTexto = (url) => {
	fetch(url)
		.then((response) => {
			if (!response.ok) {
				throw new Error(`Error HTTP: ${response.status}`);
			}

			return response.json();
		})
		.then((data) => {
			const parrafo = document.querySelector("#ej1 > p");
			const text = data.results.map((pokemon) => pokemon.name).join(", ");
			if (parrafo) {
				parrafo.innerHTML = text;
			}
		})
		.catch((error) => {
			const parrafo = document.querySelector("#ej1 > p");
			if (parrafo) {
				parrafo.innerHTML = error.message;
			}
		})
}

cargarTexto("https://pokeapi.co/api/v2/pokemon?limit=151")


// Ejercicio 2:
const cargarTexto2 = async (url) => {
	try {
		const response = await fetch(url);

		if (!response.ok) {
			throw new Error(`Error HTTP: ${response.status}`);
		}

		const data = await response.json();

		const nombres = data.results.map((pokemon) => pokemon.name).join(", ");
		const parrafo = document.querySelector("#ej2 > p");
		if (parrafo) {
			parrafo.innerHTML = nombres;
		}
	} catch (error)  {
		const parrafo = document.querySelector("#ej2 > p");
		if (parrafo) {
			parrafo.innerHTML = error.message;
		}
	}
}

cargarTexto2("https://pokeapi.co/api/v2/pokemon?limit=151")