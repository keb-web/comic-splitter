// import { useRef, useEffect } from 'react';
import { Stage, Layer, Rect } from 'react-konva';
// we need to get imagees and draw depending info from template
// need to see if dran things on canvas can be resized and how to dynamically
// update template when it is resized

// this is done alerayd with react-konva just implement it!

function CanvasPreview({splitTemplate, splitImages}){
	console.log('splitTemplate', splitTemplate)
	console.log('splitImages', splitImages)

	return(
		<>
		</>
	)
}

export default CanvasPreview

// <Stage width={window.innerWidth} height={window.innerHeight}>
//   <Layer>
// 	<Rect
// 	  x={0}
// 	  y={0}
// 	  width={window.innerWidth / 2}
// 	  height={window.innerHeight / 2}
// 	  fill="green"
// 	  stroke="white"
// 	  strokeWidth={2}
// 	/>
//   </Layer>
// </Stage>

