// Layer: Hook — stateful React hook consumed by Layer 1 (App)
import { useState, useCallback } from 'react';

// -------------------- useTweaks ----------- START ----------
// -- Calls : setTweak
// -- Called by: App
export function useTweaks(defaults) {
  const [values, setValues] = useState(defaults);

  // -------------------- setTweak ----------- START ----------
  // -- Calls : nothing (leaf)
  // -- Called by: useTweaks, App (via returned setter)
  const setTweak = useCallback((keyOrEdits, val) => {
    const edits = typeof keyOrEdits === 'object' && keyOrEdits !== null
      ? keyOrEdits
      : { [keyOrEdits]: val };
    setValues((prev) => ({ ...prev, ...edits }));
  }, []);
  //-------------------- setTweak ------------- END ----------------

  return [values, setTweak];
}
//-------------------- useTweaks ------------- END ----------------
