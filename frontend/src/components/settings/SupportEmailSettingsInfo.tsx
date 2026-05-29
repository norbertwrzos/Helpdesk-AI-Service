export default function SupportEmailSettingsInfo() {
  return (
    <div className="rounded-xl border border-cyan-500/20 bg-gray-900/60 p-5">
      <div className="flex items-start gap-3">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth={1.8}
          className="w-5 h-5 text-cyan-400 mt-0.5 shrink-0"
        >
          <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
          <polyline points="22,6 12,13 2,6" />
        </svg>
        <div className="space-y-1">
          <div className="text-sm font-medium text-cyan-300">Skrzynka e-mail supportu</div>
          <p className="text-xs text-gray-400 leading-relaxed">
            Zgłoszenia wysłane na skrzynkę supportu są rejestrowane jako tickety ze źródłem{' '}
            <span className="font-mono text-gray-300">email</span>.
          </p>
          <p className="text-xs text-gray-500 leading-relaxed">
            Import odbywa się automatycznie przez backend (IMAP/GreenMail). Tickety pojawiają się
            na liście zgłoszeń po pomyślnym imporcie.
          </p>
        </div>
      </div>
    </div>
  )
}
