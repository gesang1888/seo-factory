<?php

namespace App\Http\Controllers;

use App\Http\Middleware\DomainLocale;
use App\Services\ProductService;

class HomeController
{
    public function index(): void
    {
        header('Cache-Control: no-cache, must-revalidate');
        $config = DomainLocale::handle();
        $service = new ProductService();
        $products = $service->featured($config, 8);
        $faqs = $this->faqs($config);
        if (class_exists(\App\Services\DestLocal::class)) {
            $faqs = array_merge($faqs, \App\Services\DestLocal::faqs());
        }

        $faqSchema = [
            '@context' => 'https://schema.org',
            '@type' => 'FAQPage',
            'mainEntity' => array_map(function ($f) {
                return [
                    '@type' => 'Question',
                    'name' => $f['q'],
                    'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']],
                ];
            }, $faqs),
        ];
        $data = [
            'config' => $config,
            'products' => $products,
            'categories' => categories_for_locale($config['lang'], $config['full_site']),
            'faqs' => $faqs,
            'page_title' => __t('meta_title', ['country' => $config['country']]),
            'meta_desc' => __t('meta_desc', ['country' => $config['country']]),
            'robots' => 'index, follow',
            'faq_schema' => json_encode($faqSchema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE),
        ];
        $data['content'] = view('home', $data);
        echo view('layouts.app', $data);
    }

    private function faqs(array $config): array
    {
        $keys = ['faq_q1', 'faq_a1', 'faq_q2', 'faq_a2', 'faq_q3', 'faq_a3', 'faq_q4', 'faq_a4', 'faq_q5', 'faq_a5'];
        $faqs = [];
        for ($i = 1; $i <= 5; $i++) {
            $faqs[] = [
                'q' => __t('faq_q' . $i),
                'a' => __t('faq_a' . $i),
            ];
        }
        return $faqs;
    }
}
