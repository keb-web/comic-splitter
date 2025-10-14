// we need to get imagees and draw depending info from template
// need to see if dran things on canvas can be resized and how to dynamically
// update template when it is resized

// this is done already with react-konva just implement it!

import { useEffect, useMemo } from 'react';
import { Stage, Layer, Rect, Image} from 'react-konva';
import useImage from 'use-image'


function CanvasPreview({splitTemplate, splitImages, className}){
	let x = 0
	let width = 0
	let height = 0
	let y = 0
	if (splitTemplate.pages){
		const testTemplate = splitTemplate.pages[0].panels[0]
		x = testTemplate.x
		width = testTemplate.width
		height = testTemplate.height
		y = testTemplate.y
	}

	const filetype = splitTemplate.filetype
	function base64ToImageUrl(base64) {
		const binary = atob(base64);
		const len = binary.length;
		const bytes = new Uint8Array(len);
		for (let i = 0; i < len; i++) bytes[i] = binary.charCodeAt(i);
		const blob = new Blob([bytes], { type: filetype });
		return URL.createObjectURL(blob);
	};

	const splitImageURLS = useMemo(() => {
		if (!splitImages) return [];
		return splitImages.map(bytes => base64ToImageUrl(bytes));
	}, [splitImages, filetype]);

	useEffect(() => {
	  return () => splitImageURLS.forEach((url) => URL.revokeObjectURL(url));
	}, [splitImageURLS]);

	let testImg = splitImageURLS[0];

	const URLImage = ({src, ...rest}) => {
		let [image] = useImage(src, 'anonymous')
		return <Image image={image} {...rest}/>
	}
	
	return(
		<div className={className}>
			<Stage width={x+width} height={y+height}>
				<Layer>
					<Rect x={x} width={width} y={y} height={height} stroke='green'></Rect>
				</Layer>
				<Layer>
					<URLImage src={testImg} x={x} y={y} width={width} height={height}/>
				</Layer>
			</Stage>
		</div>
	)
}

export default CanvasPreview
