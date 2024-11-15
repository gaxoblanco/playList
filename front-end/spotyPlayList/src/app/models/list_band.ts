export interface ListBand {
  band_id: string;
  name: string;
  top_tracks?: top_track[];
  href?: string;
  img?: string;
  genres?: string[];
  img_zone?: [number, number, number, number];
}

export interface optionBand {
  name: string;
  img?: string;
  band_id?: string;
  img_zone: string;
}

interface top_track {
  name: string;
  url: string;
  img_zone?: [number, number, number, number];
}
