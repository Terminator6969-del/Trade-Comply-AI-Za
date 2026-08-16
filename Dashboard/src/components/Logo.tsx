export function Logo({ size = 32, className = "" }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      className={className}
      aria-hidden
    >
      <rect width="32" height="32" rx="9" fill="#0F2B24" />
      <path
        d="M16 6.4 24.2 10.2v6.6c0 4.9-3.5 9.2-8.2 10.6C11.3 26 7.8 21.7 7.8 16.8v-6.6L16 6.4Z"
        stroke="#A3E635"
        strokeWidth="1.55"
        strokeLinejoin="round"
      />
      <path
        d="M16 12.1v8.2M13.1 15.4 16 12.1l2.9 3.3"
        stroke="#A3E635"
        strokeWidth="1.55"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
