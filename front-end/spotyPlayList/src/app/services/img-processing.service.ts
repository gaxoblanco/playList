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

  // Método para comprimir imagen antes de guardar
  compressImage(file: File): Promise<string> {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          // Redimensionar a máximo 400px (ajusta según necesites)
          const maxSize = 400;
          let width = img.width;
          let height = img.height;

          if (width > height && width > maxSize) {
            height = (height * maxSize) / width;
            width = maxSize;
          } else if (height > maxSize) {
            width = (width * maxSize) / height;
            height = maxSize;
          }

          const canvas = document.createElement('canvas');
          canvas.width = width;
          canvas.height = height;

          const ctx = canvas.getContext('2d');
          ctx?.drawImage(img, 0, 0, width, height);

          // Calidad al 60% (0.6)
          resolve(canvas.toDataURL('image/jpeg', 0.6));
        };
        img.src = e.target?.result as string;
      };
      reader.readAsDataURL(file);
    });
  }

  base64ToFile(base64String: string, filename: string): File {
    const arr = base64String.split(',');
    const match = arr[0].match(/:(.*?);/);
    const mime = match ? match[1] : 'image/jpeg';
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);

    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }

    return new File([u8arr], filename, { type: mime });
  }
}
