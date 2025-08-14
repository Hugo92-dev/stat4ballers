/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    forceSwcTransforms: false,
  },
  swcMinify: false,
  webpack: (config, { dev, isServer }) => {
    if (dev && !isServer) {
      config.cache = false;
      config.optimization = {
        ...config.optimization,
        splitChunks: false,
        minimize: false,
      };
    }
    return config;
  },
};

module.exports = nextConfig;