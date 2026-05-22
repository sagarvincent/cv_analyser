// Layer: 1 (devtools) — draggable panel that orchestrates TweakSection / TweakRadio / TweakButton
import { useState, useRef, useCallback, useEffect } from 'react';

const STYLE = `
  .twk-panel{position:fixed;right:16px;bottom:16px;z-index:2147483646;width:280px;
    max-height:calc(100vh - 32px);display:flex;flex-direction:column;
    background:rgba(250,249,247,.78);color:#29261b;
    -webkit-backdrop-filter:blur(24px) saturate(160%);backdrop-filter:blur(24px) saturate(160%);
    border:.5px solid rgba(255,255,255,.6);border-radius:14px;
    box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 12px 40px rgba(0,0,0,.18);
    font:11.5px/1.4 ui-sans-serif,system-ui,-apple-system,sans-serif;overflow:hidden}
  .twk-hd{display:flex;align-items:center;justify-content:space-between;padding:10px 8px 10px 14px;cursor:move;user-select:none}
  .twk-hd b{font-size:12px;font-weight:600;letter-spacing:.01em}
  .twk-x{appearance:none;border:0;background:transparent;color:rgba(41,38,27,.55);width:22px;height:22px;border-radius:6px;cursor:pointer;font-size:13px;line-height:1}
  .twk-x:hover{background:rgba(0,0,0,.06);color:#29261b}
  .twk-body{padding:2px 14px 14px;display:flex;flex-direction:column;gap:10px;overflow-y:auto;overflow-x:hidden;min-height:0}
  .twk-sect{font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:rgba(41,38,27,.45);padding:10px 0 0}
  .twk-sect:first-child{padding-top:0}
  .twk-row{display:flex;flex-direction:column;gap:5px}
  .twk-lbl{display:flex;justify-content:space-between;align-items:baseline;color:rgba(41,38,27,.72)}
  .twk-lbl>span:first-child{font-weight:500}
  .twk-seg{position:relative;display:flex;padding:2px;border-radius:8px;background:rgba(0,0,0,.06);user-select:none}
  .twk-seg-thumb{position:absolute;top:2px;bottom:2px;border-radius:6px;background:rgba(255,255,255,.9);box-shadow:0 1px 2px rgba(0,0,0,.12);transition:left .15s cubic-bezier(.3,.7,.4,1),width .15s}
  .twk-seg button{appearance:none;position:relative;z-index:1;flex:1;border:0;background:transparent;color:inherit;font:inherit;font-weight:500;min-height:22px;border-radius:6px;cursor:pointer;padding:4px 6px;line-height:1.2}
  .twk-btn{appearance:none;height:26px;padding:0 12px;border:0;border-radius:7px;background:rgba(0,0,0,.78);color:#fff;font:inherit;font-weight:500;cursor:pointer}
  .twk-btn:hover{background:rgba(0,0,0,.88)}
`;

// -------------------- TweaksPanel ----------- START ----------
// -- Calls : clamp, onDragStart
// -- Called by: App
export function TweaksPanel({ title = 'Tweaks', children }) {
  const [open, setOpen] = useState(false);
  const dragRef = useRef(null);
  const offsetRef = useRef({ x: 16, y: 16 });

  // -------------------- clamp ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: TweaksPanel, onDragStart
  const clamp = useCallback(() => {
    const panel = dragRef.current;
    if (!panel) return;
    const w = panel.offsetWidth, h = panel.offsetHeight;
    const maxR = Math.max(16, window.innerWidth - w - 16);
    const maxB = Math.max(16, window.innerHeight - h - 16);
    offsetRef.current = {
      x: Math.min(maxR, Math.max(16, offsetRef.current.x)),
      y: Math.min(maxB, Math.max(16, offsetRef.current.y)),
    };
    panel.style.right = offsetRef.current.x + 'px';
    panel.style.bottom = offsetRef.current.y + 'px';
  }, []);
  //-------------------- clamp ------------- END ----------------

  useEffect(() => { if (open) clamp(); }, [open, clamp]);

  // -------------------- onDragStart ----------- START ----------
  // -- Calls : clamp
  // -- Called by: TweaksPanel (drag header mousedown)
  const onDragStart = (e) => {
    const panel = dragRef.current;
    if (!panel) return;
    const r = panel.getBoundingClientRect();
    const startRight = window.innerWidth - r.right;
    const startBottom = window.innerHeight - r.bottom;
    const sx = e.clientX, sy = e.clientY;
    const move = (ev) => {
      offsetRef.current = { x: startRight - (ev.clientX - sx), y: startBottom - (ev.clientY - sy) };
      clamp();
    };
    const up = () => { window.removeEventListener('mousemove', move); window.removeEventListener('mouseup', up); };
    window.addEventListener('mousemove', move);
    window.addEventListener('mouseup', up);
  };
  //-------------------- onDragStart ------------- END ----------------

  if (!open) {
    return (
      <button onClick={() => setOpen(true)} style={{
        position: 'fixed', right: 16, bottom: 16, zIndex: 2147483646,
        background: 'rgba(250,249,247,.85)', border: '.5px solid rgba(255,255,255,.6)',
        borderRadius: 10, padding: '8px 12px', cursor: 'pointer',
        font: '11.5px/1 ui-sans-serif,system-ui,sans-serif', fontWeight: 600,
        color: '#29261b', backdropFilter: 'blur(12px)',
        boxShadow: '0 4px 16px rgba(0,0,0,.15)',
      }}>⚙ Tweaks</button>
    );
  }

  return (
    <>
      <style>{STYLE}</style>
      <div ref={dragRef} className="twk-panel" style={{ right: offsetRef.current.x, bottom: offsetRef.current.y }}>
        <div className="twk-hd" onMouseDown={onDragStart}>
          <b>{title}</b>
          <button className="twk-x" onClick={() => setOpen(false)}>✕</button>
        </div>
        <div className="twk-body">{children}</div>
      </div>
    </>
  );
}
//-------------------- TweaksPanel ------------- END ----------------
