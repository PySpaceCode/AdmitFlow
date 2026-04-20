import { Navbar } from "@/components/Navbar";
import { HeroSection } from "@/components/HeroSection";
import { ProblemSolutionSection } from "@/components/ProblemSolutionSection";
import { FeaturesSection } from "@/components/FeaturesSection";
import { WorkflowVisual } from "@/components/WorkflowVisual";
import { PricingSection } from "@/components/PricingSection";
import { TestimonialsSection } from "@/components/TestimonialsSection";
import { OfferSection } from "@/components/OfferSection";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <div className="min-h-screen bg-background font-[family-name:var(--font-sans)]">
      <Navbar />
      <main className="flex-1">
        <HeroSection />
        <ProblemSolutionSection />
        <FeaturesSection />
        <WorkflowVisual />
        <PricingSection />
        <TestimonialsSection />
        <OfferSection />
      </main>
      <Footer />
    </div>
  );
}
