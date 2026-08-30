import entriesJson from "../data/entries.json";
import metaJson from "../data/meta.json";

export interface Entry {
  /** Permanent register number, assigned by build_site_data.py and stable across sorts. */
  no: number;
  slug: string;
  name: string;
  occupation: string;
  field: string;
  country: string;
  organization: string;
  life: string;
  connection: string;
  origin: string;
  context: string;
  source: string;
  sourceLabel: string;
  nameSource: string;
  /** Hidden search words, never rendered. */
  tags: string;
  ironic: boolean;
  translation: boolean;
  related: string[];
}

export interface Field {
  slug: string;
  label: string;
  count: number;
}

export interface Meta {
  total: number;
  researched: number;
  rejected: number;
  fields: Field[];
  countries: number;
  ironic: number;
  translation: number;
  earliestBirth: number;
  latestBirth: number;
  span: number;
}

export const entries = entriesJson as Entry[];
export const meta = metaJson as Meta;

const bySlug = new Map(entries.map((e) => [e.slug, e]));

export function get(slug: string): Entry {
  const entry = bySlug.get(slug);
  if (!entry) throw new Error(`no entry for slug ${slug}`);
  return entry;
}

export function fieldLabel(slug: string): string {
  return meta.fields.find((f) => f.slug === slug)?.label ?? slug;
}

export function inField(slug: string): Entry[] {
  return entries.filter((e) => e.field === slug);
}

export const ironic = entries.filter((e) => e.ironic);

/** Alphabetical by surname-ish: the last word of the name, which is what people scan for. */
export function alphabetical(list: Entry[]): Entry[] {
  return [...list].sort((a, b) => {
    const key = (e: Entry) => {
      const parts = e.name.replace(/["']/g, "").split(" ");
      return `${parts[parts.length - 1]} ${parts[0]}`.toLowerCase();
    };
    return key(a).localeCompare(key(b));
  });
}

/** Sort key for the A-Z control: surname first, which is what people scan for. */
export const surnameKey = (e: Entry): string => {
  const parts = e.name.replace(/["']/g, "").split(" ");
  return `${parts[parts.length - 1]} ${parts[0]}`.toLowerCase();
};

export const canonical = (path: string) => new URL(path, "https://theirnames.fit").href;
