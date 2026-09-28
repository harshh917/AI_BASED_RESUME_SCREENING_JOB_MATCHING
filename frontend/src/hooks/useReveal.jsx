import { useEffect, useRef, useState } from 'react'

export function useInView(threshold = 0.15) {
  const ref = useRef(null)
  const [inView, setInView] = useState(false)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setInView(true); io.disconnect() } }, { threshold })
    io.observe(el)
    return () => io.disconnect()
  }, [threshold])
  return [ref, inView]
}

export function Reveal({ children, delay = 0, className = '' }) {
  const [ref, inView] = useInView()
  return <div ref={ref} style={{ '--d': `${delay}ms` }} className={`reveal ${inView ? 'in' : ''} ${className}`}>{children}</div>
}

export function CountUp({ to, suffix = '', duration = 1400 }) {
  const [ref, inView] = useInView(0.4)
  const [val, setVal] = useState(0)
  useEffect(() => {
    if (!inView) return
    let raf, start
    const tick = (t) => {
      start ??= t
      const p = Math.min((t - start) / duration, 1)
      setVal(Math.round((1 - Math.pow(1 - p, 3)) * to))
      if (p < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [inView, to, duration])
  return <span ref={ref}>{val}{suffix}</span>
}
