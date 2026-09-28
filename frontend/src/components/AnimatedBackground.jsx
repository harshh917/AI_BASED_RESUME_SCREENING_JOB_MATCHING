// Light pastel animated backdrop: shifting gradient sky, soft colour blobs, grid, rising bubbles.
const COLORS = ['#a5b4fc', '#f9a8d4', '#67e8f9', '#fcd34d', '#86efac', '#c4b5fd']
const PARTICLES = Array.from({ length: 20 }, (_, i) => ({
  left: (i * 37) % 100,
  size: 8 + (i % 5) * 5,
  delay: -((i * 1.9) % 18),
  dur: 14 + (i % 6) * 3,
  color: COLORS[i % COLORS.length],
}))

export default function AnimatedBackground() {
  return (
    <div aria-hidden className="pointer-events-none fixed inset-0 z-0 overflow-hidden">
      <div className="pastel-sky absolute inset-0" />
      <div className="animate-blob absolute -left-32 -top-24 h-[30rem] w-[30rem] rounded-full bg-sky-300/50 blur-3xl" />
      <div className="animate-blob absolute -right-24 top-1/4 h-[28rem] w-[28rem] rounded-full bg-pink-300/45 blur-3xl [animation-delay:-6s]" />
      <div className="animate-blob absolute bottom-[-8rem] left-1/3 h-[26rem] w-[26rem] rounded-full bg-amber-200/60 blur-3xl [animation-delay:-11s]" />
      <div className="animate-blob absolute bottom-10 -left-20 h-72 w-72 rounded-full bg-emerald-200/50 blur-3xl [animation-delay:-3s]" />
      <div className="bg-grid absolute inset-0" />
      {PARTICLES.map((p, i) => (
        <span key={i} className="particle absolute bottom-[-30px] rounded-full"
          style={{ left: `${p.left}%`, width: p.size, height: p.size, background: p.color, opacity: 0.7, border: '1px solid rgba(255,255,255,.9)', animationDelay: `${p.delay}s`, animationDuration: `${p.dur}s` }} />
      ))}
    </div>
  )
}
