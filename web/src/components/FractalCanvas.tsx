import { useEffect, useRef } from "react";

interface FractalCanvasProps {
  /** Base hue (0-360) the palette cycles around. Lets each OS module tint the fractal. */
  hue?: number;
  /** Internal render resolution in pixels. Lower = faster, softer glow. */
  resolution?: number;
  /** Max iterations per pixel. Higher = more detail, more CPU. */
  iterations?: number;
}

/**
 * A living Julia-set fractal that slowly evolves and gently responds to touch/pointer.
 * Rendered at a low internal resolution and scaled up by the browser for a soft,
 * luminous "looking into your own mind" effect that stays smooth on mobile.
 */
export default function FractalCanvas({
  hue = 265,
  resolution = 220,
  iterations = 48,
}: FractalCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pointerRef = useRef({ x: 0, y: 0, target: { x: 0, y: 0 } });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d", { alpha: false });
    if (!ctx) return;

    const RES = resolution;
    canvas.width = RES;
    canvas.height = RES;

    const baseHue = hue;
    let raf = 0;
    let lastFrame = 0;
    let t = 0;

    const handlePointer = (clientX: number, clientY: number) => {
      const rect = canvas.getBoundingClientRect();
      pointerRef.current.target = {
        x: (clientX - rect.left) / rect.width - 0.5,
        y: (clientY - rect.top) / rect.height - 0.5,
      };
    };

    const onMouseMove = (e: MouseEvent) => handlePointer(e.clientX, e.clientY);
    const onTouchMove = (e: TouchEvent) => {
      const touch = e.touches[0];
      if (touch) handlePointer(touch.clientX, touch.clientY);
    };

    window.addEventListener("mousemove", onMouseMove, { passive: true });
    window.addEventListener("touchmove", onTouchMove, { passive: true });

    const hslToRgb = (h: number, s: number, l: number): [number, number, number] => {
      const a = s * Math.min(l, 1 - l);
      const f = (n: number) => {
        const k = (n + h / 30) % 12;
        return l - a * Math.max(-1, Math.min(k - 3, 9 - k, 1));
      };
      return [Math.round(f(0) * 255), Math.round(f(8) * 255), Math.round(f(4) * 255)];
    };

    const render = (now: number) => {
      raf = requestAnimationFrame(render);
      // throttle heavy fractal recompute to ~12fps; CSS/GPU handles smoothing
      if (now - lastFrame < 80) return;
      lastFrame = now;

      // ease pointer toward target for a calm "drift"
      pointerRef.current.x += (pointerRef.current.target.x - pointerRef.current.x) * 0.04;
      pointerRef.current.y += (pointerRef.current.target.y - pointerRef.current.y) * 0.04;

      const image = ctx.createImageData(RES, RES);
      const data = image.data;

      // Julia constant slowly orbits, nudged by pointer position
      const cx = -0.74 + 0.06 * Math.sin(t * 0.11) + pointerRef.current.x * 0.18;
      const cy = 0.18 + 0.06 * Math.cos(t * 0.08) + pointerRef.current.y * 0.18;

      const zoom = 1.55 + 0.18 * Math.sin(t * 0.05);
      const rot = t * 0.015;
      const cosR = Math.cos(rot);
      const sinR = Math.sin(rot);

      for (let py = 0; py < RES; py++) {
        const y0n = py / RES - 0.5;
        for (let px = 0; px < RES; px++) {
          const x0n = px / RES - 0.5;

          const x0 = (x0n * cosR - y0n * sinR) * zoom;
          const y0 = (x0n * sinR + y0n * cosR) * zoom;

          let zx = x0;
          let zy = y0;
          let iter = 0;
          while (zx * zx + zy * zy < 4 && iter < iterations) {
            const xt = zx * zx - zy * zy + cx;
            zy = 2 * zx * zy + cy;
            zx = xt;
            iter++;
          }

          const idx = (py * RES + px) * 4;
          if (iter >= iterations) {
            data[idx] = 4;
            data[idx + 1] = 2;
            data[idx + 2] = 14;
            data[idx + 3] = 255;
          } else {
            const smooth = iter + 1 - Math.log2(Math.log2(zx * zx + zy * zy + 1e-9));
            const v = Math.max(0, Math.min(1, smooth / iterations));
            const hueShift = (baseHue + v * 80 + t * 6) % 360;
            const [r, g, b] = hslToRgb(hueShift, 0.75, 0.18 + v * 0.55);
            data[idx] = r;
            data[idx + 1] = g;
            data[idx + 2] = b;
            data[idx + 3] = 255;
          }
        }
      }

      ctx.putImageData(image, 0, 0);
      t += 0.045;
    };

    raf = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("touchmove", onTouchMove);
    };
  }, [hue, resolution, iterations]);

  return <canvas ref={canvasRef} className="fractal-canvas" aria-hidden="true" />;
}
