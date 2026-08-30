import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { Resvg } from "@resvg/resvg-js";
import satori from "satori";

/**
 * Satori needs the raw TTF, and this module gets bundled into dist/ during the build, so a
 * path relative to import.meta.url stops pointing at anything. Walk up from the working
 * directory instead, which lands on the project root whether that is site/ or the repo root.
 */
function font(file: string): Buffer {
  let dir = resolve(process.cwd());
  for (let up = 0; up < 4; up++) {
    const path = join(dir, "fonts", file);
    if (existsSync(path)) return readFileSync(path);
    dir = dirname(dir);
  }
  throw new Error(`cannot find fonts/${file} from ${process.cwd()}`);
}

const fonts = [
  { name: "Courier", data: font("CourierPrime-Regular.ttf"), weight: 400 as const, style: "normal" as const },
  { name: "Courier", data: font("CourierPrime-Bold.ttf"), weight: 700 as const, style: "normal" as const },
];

const PAPER = "#f4f2ea";
const INK = "#16150f";
const FAINT = "#8b8779";
const STAMP = "#a8351f";

const WIDTH = 1200;
const HEIGHT = 630;
const PAD = 72;
const INNER = WIDTH - PAD * 2;

/** Courier Prime is monospaced at 0.6em per character, which is what makes the leader work. */
const ADVANCE = 0.6;
const colsAt = (size: number) => Math.floor(INNER / (ADVANCE * size));

/**
 * The card is one line out of the register: name, a run of dots, trade. In a monospaced face
 * the dots can just be typed, so the leader is real text rather than a drawn rule, and the
 * whole thing reads like a line off a printout.
 *
 * Long pairs will not fit on one line at a size worth looking at, so those stack instead.
 */
function leaderLine(name: string, trade: string, size: number): string {
  const dots = colsAt(size) - name.length - trade.length - 2;
  return `${name} ${".".repeat(Math.max(3, dots))} ${trade}`;
}

function fit(name: string, trade: string): { size: number; oneLine: boolean } {
  const need = name.length + trade.length + 6;
  const size = Math.floor(INNER / (need * ADVANCE));
  if (size >= 30) return { size: Math.min(size, 58), oneLine: true };
  // Stacked: the name sets its own size, the trade sits under it.
  const nameSize = Math.min(Math.floor(INNER / (name.length * ADVANCE)), 84);
  return { size: Math.max(nameSize, 28), oneLine: false };
}

const text = (
  content: string,
  style: Record<string, string | number>,
): Record<string, unknown> => ({
  type: "div",
  props: { style: { fontFamily: "Courier", ...style }, children: content },
});

const rule = (children: unknown[], extra: Record<string, string | number> = {}) => ({
  type: "div",
  props: {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "flex-end",
      fontFamily: "Courier",
      fontSize: "22px",
      letterSpacing: "0.14em",
      color: FAINT,
      ...extra,
    },
    children,
  },
});

interface Card {
  name: string;
  occupation: string;
  /** The register number, printed top right the way an entry page prints it. */
  no?: number;
  footer?: string;
}

export async function card({ name, occupation, no, footer }: Card): Promise<Buffer> {
  const trade = occupation.toLowerCase();
  const { size, oneLine } = fit(name, trade);

  const body = oneLine
    ? [text(leaderLine(name, trade, size), { fontSize: `${size}px`, color: INK })]
    : [
        text(name, { fontSize: `${size}px`, lineHeight: 1.05, color: INK }),
        text(`${".".repeat(8)} ${trade}`, {
          fontSize: `${Math.max(Math.round(size * 0.42), 24)}px`,
          color: INK,
          marginTop: "18px",
        }),
      ];

  const svg = await satori(
    {
      type: "div",
      props: {
        style: {
          width: `${WIDTH}px`,
          height: `${HEIGHT}px`,
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          backgroundColor: PAPER,
          padding: `${PAD}px`,
        },
        children: [
          rule(
            [
              text("THEIR NAMES FIT", { letterSpacing: "0.14em" }),
              text(no ? `ENTRY NO. ${String(no).padStart(3, "0")}` : "A REGISTER OF APTRONYMS", {
                letterSpacing: "0.14em",
              }),
            ],
            { borderBottom: `2px solid ${INK}`, paddingBottom: "16px", color: INK },
          ),
          {
            type: "div",
            props: {
              style: {
                display: "flex",
                flexDirection: "column",
                flex: 1,
                justifyContent: "center",
              },
              children: body,
            },
          },
          rule([
            text(footer ?? "CHECKED", { letterSpacing: "0.18em", color: STAMP, fontWeight: 700 }),
            text("theirnames.fit", { letterSpacing: "0.06em" }),
          ]),
        ],
      },
    },
    { width: WIDTH, height: HEIGHT, fonts },
  );

  return new Resvg(svg, { fitTo: { mode: "width", value: WIDTH } }).render().asPng();
}
