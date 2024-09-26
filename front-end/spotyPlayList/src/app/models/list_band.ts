export interface ListBand {
  band_id: string;
  name: string;
  top_tracks?: top_track[];
  href?: string;
}

interface top_track {
  name: string;
  url: string;
}
