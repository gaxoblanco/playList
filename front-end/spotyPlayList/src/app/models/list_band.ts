export interface ListBand {
  band_id: string;
  name: string;
  top_tracks?: top_track[];
  href?: string;
  img_url?: string;
  genres?: string[];
  img_zone: [number, number, number, number];
}

export interface optionBand {
  name: string;
  img_url?: string;
  band_id?: string;
  img_zone: string;
}

interface top_track {
  name: string;
  url: string;
}
