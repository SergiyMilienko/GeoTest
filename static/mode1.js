function handleCountryClick(countryName) {
    document.getElementById("countryInput").value = countryName; 
    document.forms[0].submit();
}

window.addEventListener('DOMContentLoaded', function() {
    var svgElement = document.querySelector('.mapdiv svg');
    var zoomLevel = 1;
    var isDragging = false;
    var prevX = 0;
    var prevY = 0;
    var viewBoxX = 0;
    var viewBoxY = 0;

    function zoomIn() {
        zoomLevel = Math.min(zoomLevel + 1, 20);
        updateZoom();
    }

    function zoomOut() {
        zoomLevel = Math.max(zoomLevel - 1, 1);
        updateZoom();
    }

    function updateZoom() {
        svgElement.style.transform = `scale(${zoomLevel})`;
    }

    function handleMouseWheel(event) {
        event.preventDefault();
        var delta = Math.max(-1, Math.min(1, -(event.deltaY || -event.detail)));
        if (delta > 0) {
            zoomIn();
        } else {
            zoomOut();
        }
    }

    function handleMouseDown(event) {
        isDragging = true;
        prevX = event.clientX;
        prevY = event.clientY;
    }

    function handleMouseUp(event) {
        isDragging = false;
    }

    function handleMouseMove(event)  {
        if (isDragging) {
            var newX = prevX - event.clientX;
            var newY = prevY - event.clientY;
            prevX = event.clientX;
            prevY = event.clientY;
            viewBoxX += newX / zoomLevel;
            viewBoxY += newY / zoomLevel;
            svgElement.setAttribute("viewBox", `${viewBoxX} ${viewBoxY} 2000 857`);
        }
    }

    document.querySelector('.zoom-controls .zoom-in').addEventListener('click', zoomIn);
    document.querySelector('.zoom-controls .zoom-out').addEventListener('click', zoomOut);
    document.addEventListener('wheel', handleMouseWheel);
    document.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
});