// Agregado dentro de DOMContentLoaded para garantizar que el DOM esté cargado completamente
document.addEventListener("DOMContentLoaded", function() {
    const syntaxNetworkContainer = document.getElementById("network-morph");
    const syntaxButton = document.getElementById('ButtomMorph');
    const progressBar = document.getElementById('progressBar');

    function clearContainer(container) {
        if (container) {
            container.innerHTML = '';
        } else {
            console.error("El contenedor no existe en el DOM.");
        }
    }

    syntaxButton.addEventListener('click', syntaxProcess);

    function syntaxProcess() {
        var textInput = document.getElementById("text-1").value;
        if (!textInput.trim()) {
            console.error("El texto para analizar no puede estar vacío.");
            return; // Detener la ejecución si el texto está vacío
        }

        // Iniciar la barra de progreso
        progressBar.style.width = '0%'; // Reiniciar la barra de progreso
        progressBar.style.display = 'block'; // Mostrar la barra

        fetch('https://5f6b6akff7.execute-api.us-east-2.amazonaws.com/DEV/AIdeaText_Comprehend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: textInput }),
        })
        .then(response => response.json())
        .then(data => {
            let progress = 0;
            const interval = setInterval(() => {
                progress += 10; // Incrementar progreso más lentamente
                progressBar.style.width = progress + '%';

                if (progress >= 100) {
                    clearInterval(interval);
                    progressBar.style.width = '100%';
                    setTimeout(() => { progressBar.style.display = 'none'; }, 500);

                    if (data.syntax && data.syntax.nodes) {
                        visualizeSyntaxTreemap(data.syntax, syntaxNetworkContainer);
                    } else {
                        console.error("Error: No se encontraron datos de análisis sintáctico válidos en la respuesta del servidor.");
                    }
                }
            }, 200); // Modifica este tiempo según la duración esperada del proceso
        })
        .catch(error => {
            console.error("Error al procesar el texto:", error);
            clearInterval(interval);
            progressBar.style.width = '100%';
            progressBar.style.backgroundColor = 'red';
        });
    }

function visualizeSyntaxTreemap(syntaxData) {
    clearContainer(syntaxNetworkContainer);

    if (!syntaxData || !syntaxData.nodes) {
        console.error("Error: No se encontraron datos de análisis sintáctico válidos.");
        return;
    }

    // Definir dimensiones para el treemap y la leyenda
    const containerWidth = syntaxNetworkContainer.clientWidth;
    const containerHeight = syntaxNetworkContainer.clientHeight - 50; // Reserva espacio para la leyenda

    // Crear SVG para el treemap
    const svgTreemap = d3.select(syntaxNetworkContainer).append("svg")
        .attr("width", containerWidth)
        .attr("height", containerHeight)
        .style("font", "10px sans-serif");

    // Crear el treemap
    const treemap = d3.treemap()
        .size([containerWidth, containerHeight])
        .paddingInner(1)
        .paddingOuter(3);

    const hierarchyData = buildHierarchy(syntaxData.nodes);
    const root = d3.hierarchy(hierarchyData)
        .sum(d => d.value)
        .sort((a, b) => b.height - a.height || b.value - a.value);

    treemap(root);

    const leaf = svgTreemap.selectAll("g")
        .data(root.leaves())
        .enter().append("g")
        .attr("transform", d => `translate(${d.x0},${d.y0})`);

    leaf.append("rect")
        .attr("width", d => d.x1 - d.x0)
        .attr("height", d => d.y1 - d.y0)
        .attr("fill", d => getColorByFrequency(d.data.value, d.parent.data.name))
        .attr("stroke", "black");

    leaf.append("text")
        .attr("x", 5)
        .attr("y", 15)
        .text(d => d.data.name + " [" + d.data.value + "]")
        .attr("fill", "white")
        .attr("font-size", "10px")
        .attr("font-weight", "bold");

    // Crear SVG para la leyenda en el mismo contenedor pero separado
    const svgLegend = d3.select(syntaxNetworkContainer).append("svg")
        .attr("width", containerWidth)
        .attr("height", 50) // Altura fija para la leyenda
        .style("font", "12px sans-serif");

    const legend = svgLegend.append("g")
        .attr("transform", "translate(0,20)"); // Posiciona adecuadamente dentro del SVG de la leyenda

    const categories = Object.keys(POSLabels);
    categories.forEach((key, index) => {
        const color = getColorByPOS(key);
        legend.append("rect")
            .attr("x", index * 120) // Espaciado entre elementos de la leyenda
            .attr("width", 20)
            .attr("height", 20)
            .style("fill", color);

        legend.append("text")
            .attr("x", index * 120 + 25)
            .attr("y", 15)
            .text(POSLabels[key])
            .style("text-anchor", "start")
            .style("fill", "black");
    });
}

    function getColorByFrequency(value, pos) {
        const baseColor = d3.color(getColorByPOS(pos));
        const intensity = d3.scaleLinear().domain([1, 10]).range([1, 0.5])(value);
        return baseColor.darker(intensity);
    }

    function getColorByPOS(pos) {
        const colorMap = {
            'ADP': '#ff6d6d',
            'DET': '#ff8686',
            'CONJ': '#ffa0a0',
            'CCONJ': '#ffb9b9',
            'SCONJ': '#ffd3d3',
            'ADJ': '#ffd3d3',
            'ADV': '#cccc00',
            'NOUN': '#006700',
            'VERB': '#008000',
            'PROPN': '#009a00',
            'PRON': '#00b300',
            'AUX': '#00cd00'
        };
        return colorMap[pos] || 'lightblue';
    }

    function buildHierarchy(nodes) {
        let root = { name: "root", children: [] };
        let categoryMap = {};

        nodes.forEach(node => {
            if (!categoryMap[node.type]) {
                categoryMap[node.type] = { name: node.type, children: [] };
            }
            let child = categoryMap[node.type].children.find(child => child.name === node.text);
            if (child) {
                child.value += 1;
            } else {
                categoryMap[node.type].children.push({ name: node.text, value: 1 });
            }
        });

        Object.values(categoryMap).forEach(category => {
            root.children.push(category);
        });

        return root;
    }

    const POSLabels = {
        'ADP': 'Preposición',
        'DET': 'Determinante',
        'CONJ': 'Conjunción',
        'CCONJ': 'Conjunción Coordinante',
        'SCONJ': 'Conjunción Subordinante',
        'ADJ': 'Adjetivo',
        'ADV': 'Adverbio',
        'NOUN': 'Sustantivo',
        'VERB': 'Verbo',
        'PROPN': 'Nombre Propio',
        'PRON': 'Pronombre',
        'AUX': 'Auxiliar'
    };
});
