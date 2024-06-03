document.addEventListener("DOMContentLoaded", function() {
    const morphContainer = document.getElementById("network-morph");
    const syntaxContainer = document.getElementById("network-syntax");
    const semanticContainer = document.getElementById("network-semantic");
    const discourseContainer = document.getElementById("network-discourse");

    const morphButton = document.getElementById('ButtonMorph');
    const syntaxButton = document.getElementById('ButtonSyntax');
    const semanticButton = document.getElementById('ButtonSemantic');
    const discourseButton = document.getElementById('ButtonDiscourse');

    const progressBar = document.getElementById('progressBar');

    function clearContainer(container) {
        if (container) {
            container.innerHTML = '';
        } else {
            console.error("El contenedor no existe en el DOM.");
        }
    }

    function handleProcess(button, container, textInputId, endpoint) {
        button.addEventListener('click', function() {
            var textInput = document.getElementById(textInputId).value;
            if (!textInput.trim()) {
                console.error("El texto para analizar no puede estar vacío.");
                return;
            }

            progressBar.style.width = '0%';
            progressBar.style.display = 'block';

            fetch(endpoint, {
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
                    progress += 10;
                    progressBar.style.width = progress + '%';

                    if (progress >= 100) {
                        clearInterval(interval);
                        progressBar.style.width = '100%';
                        setTimeout(() => { progressBar.style.display = 'none'; }, 500);

                        if (data.syntax && data.syntax.nodes) {
                            visualizeSyntaxTreemap(data.syntax, container);
                        } else {
                            console.error("Error: No se encontraron datos de análisis sintáctico válidos en la respuesta del servidor.");
                        }
                    }
                }, 200);
            })
            .catch(error => {
                console.error("Error al procesar el texto:", error);
                clearInterval(interval);
                progressBar.style.width = '100%';
                progressBar.style.backgroundColor = 'red';
            });
        });
    }

    handleProcess(morphButton, morphContainer, "text-1", 'https://5f6b6akff7.execute-api.us-east-2.amazonaws.com/DEV/morphAnalyzer');
    handleProcess(syntaxButton, syntaxContainer, "text-2", 'https://5f6b6akff7.execute-api.us-east-2.amazonaws.com/DEV/morphAnalyzer');
    handleProcess(semanticButton, semanticContainer, "text-3", 'https://5f6b6akff7.execute-api.us-east-2.amazonaws.com/DEV/morphAnalyzer');
    handleProcess(discourseButton, discourseContainer, "text-4", 'https://5f6b6akff7.execute-api.us-east-2.amazonaws.com/DEV/morphAnalyzer');

    function visualizeSyntaxTreemap(syntaxData, container) {
        clearContainer(container);

        if (!syntaxData || !syntaxData.nodes) {
            console.error("Error: No se encontraron datos de análisis sintáctico válidos.");
            return;
        }

        const containerWidth = container.clientWidth;
        const containerHeight = container.clientHeight - 50;

        const svgTreemap = d3.select(container).append("svg")
            .attr("width", containerWidth)
            .attr("height", containerHeight)
            .style("font", "10px sans-serif");

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
    }
});
