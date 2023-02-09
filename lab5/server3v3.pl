#!/usr/bin/perl
use HTTP::Daemon;
use HTTP::Status;  
use IO::File;

my $d = HTTP::Daemon->new(
         LocalAddr => 'localhost',
         LocalPort => 8002,
     )|| die;

print "Please contact me at: <URL:", $d->url, ">\n";



while (my $c = $d->accept) {
    while (my $r = $c->get_request) {
        if ($r->method eq 'GET') {
            my $uri = $r->uri;
            print "GET ", $uri, "\n";

            if ($uri eq "/") {
                $uri = "/index.html";
            }
			
            my $requested_file = "." . $uri;
            if ( -e $requested_file) {
                $c->send_file_response($requested_file);
            } else {
                $c->send_error(RC_NOT_FOUND);
            }
        }
         elsif($r->method eq 'POST')
        {
            print $r->as_string, "\n";
        my $response = HTTP::Response->new(200);
        $response->header("Content-Type" => "text/text");
        $response->content($r->as_string);
        $c->send_response($response);
        }
        else {
            $c->send_error(RC_FORBIDDEN)
        }
    }
    $c->close;
    undef($c);
}