import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/routecam',
  images: {
    unoptimized: true,
  }
};

export default nextConfig;
