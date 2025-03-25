import { ElementRef, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ImgProcessingService {

  constructor() { }

  calculateRatios(imgRef: ElementRef<HTMLImageElement>, imgWidth: number, imgHeight: number): { ratioX: number; ratioY: number } {
    const originalImgWidth = imgRef.nativeElement.width;
    const originalImgHeight = imgRef.nativeElement.height;

    return {
      ratioX: originalImgWidth / imgWidth,
      ratioY: originalImgHeight / imgHeight,
    };
  }

  ajustBandPositions(imgRef: ElementRef<HTMLImageElement>, zoneX: number, zoneY: number, zoneX2: number, zoneY2: number, imgWidth: number, imgHeight: number): { boxX: number; boxY: number; boxX2: number; boxY2: number } {
    const { ratioX, ratioY } = this.calculateRatios(imgRef, imgWidth, imgHeight);

    return {
      boxX: zoneX * ratioX - 5,
      boxY: zoneY * ratioY - 3,
      boxX2: zoneX2 * 3 * ratioX,
      boxY2: zoneY2 * 3 * ratioY,
    };
  }

  updatePointerPosition(imgRef: ElementRef<HTMLImageElement>, positionArray: Array<number>, imgWidth: number, imgHeight: number): { boxX: number; boxY: number } {
    const originalImgWidth = imgRef.nativeElement.width;
    const originalImgHeight = imgRef.nativeElement.height;
    const ratioX = originalImgWidth / imgWidth;
    const ratioY = originalImgHeight / imgHeight;

    return {
      boxX: positionArray[0] * ratioX,
      boxY: positionArray[1] * ratioY,
    };
  }

}
