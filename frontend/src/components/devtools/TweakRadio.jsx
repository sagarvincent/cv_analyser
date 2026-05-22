// Layer: 2 (devtools sub-component) — pure rendering
// -------------------- TweakRadio ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: App
export function TweakRadio({ label, value, options, onChange }) {
  const opts = options.map(o => typeof o === 'object' ? o : { value: o, label: o });
  const idx = Math.max(0, opts.findIndex(o => o.value === value));
  const n = opts.length;
  return (
    <div className="twk-row">
      <div className="twk-lbl"><span>{label}</span></div>
      <div className="twk-seg">
        <div className="twk-seg-thumb" style={{ left: `calc(2px + ${idx} * (100% - 4px) / ${n})`, width: `calc((100% - 4px) / ${n})` }} />
        {opts.map(o => (
          <button key={o.value} type="button" onClick={() => onChange(o.value)}>{o.label}</button>
        ))}
      </div>
    </div>
  );
}
//-------------------- TweakRadio ------------- END ----------------
