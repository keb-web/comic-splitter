// we need to get imagees and draw depending info from template
// need to see if dran things on canvas can be resized and how to dynamically
// update template when it is resized

// this is done already with react-konva just implement it!
// fix sizing image issues
// 	 full pages are being rendered based on panel sizes
// 	 if etched we just need to display the image without specifying
// 	 affix div size and do not let updates values change it

// add rectangles based on tempaltes

import { useEffect, useMemo, useState} from 'react';
import { Stage, Layer, Rect, Image} from 'react-konva';
import useImage from 'use-image'


// This Canvas Preview should only work with etched
// on crop, it should just be a simple carosel
function CanvasPreview({splitTemplate, splitImages, className, galleryHeight, galleryWidth}){

	let x = 0, width = 0, height = 0, y = 0
	if (splitTemplate.pages){
		console.log(splitTemplate)
		const testTemplate = splitTemplate.pages[0].panels[0]
		x = testTemplate.x
		width = testTemplate.width
		height = testTemplate.height
		y = testTemplate.y
		console.log(testTemplate)
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

	const URLImage = ({src, galleryWidth, galleryHeight, ...rest}) => {
		let [image] = useImage(src, 'anonymous')
  		const [scale, setScale] = useState(1);
		const [imgWidth, setImgWidth] = useState(0)
		const [imgHeight, setImgHeight] = useState(0)
		const [offsetX, setOffsetX] = useState(0)
		const [offsetY, setOffsetY] = useState(0)

        useEffect(() => {
          if (image) {
            const width = image.naturalWidth;
            const height = image.naturalHeight;

			const scaleX = galleryWidth / width;
			const scaleY = galleryHeight / height;
			const newScale = Math.min(scaleX, scaleY);
			const offsetX = (galleryWidth - width * newScale) / 2;
			const offsetY = (galleryHeight - height * newScale) / 2;

			setScale(newScale);
			setImgHeight(height);
			setImgWidth(width);
			setOffsetX(offsetX);
			setOffsetY(offsetY);

          }
        }, [image, galleryWidth, galleryHeight]);

		return <Image 
					image={image}
					x={offsetX} y={offsetY}
		  			width={imgWidth * scale} 
				    height={imgHeight * scale}
					{...rest}
				/>
	}
	
	return (
		<div className={className}>
			<Stage width={galleryWidth} height={galleryHeight}>

				<Layer className='bgLayer'>
					<URLImage src={testImg} galleryWidth={galleryWidth} galleryHeight={galleryHeight}/>
				</Layer>

				<Layer className='canvasLayer'>
					<Rect x={x} width={width} y={y} height={height} stroke='green'></Rect>
				</Layer>
			</Stage>
		</div>
	)
}

export default CanvasPreview
